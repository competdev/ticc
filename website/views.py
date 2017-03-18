from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, get_user
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import formats
from .models import *
from .forms import *
from datetime import datetime
from django.http import JsonResponse, HttpResponse
import random
import json


def home(request):
    # A parte a seguir foi feita para evitar que cada integrante tenha que criar o grupo no seu repositório remoto
    group, create = Group.objects.get_or_create(name='Judges')
    perm = []
    perm.append(Permission.objects.get(name='Can add match score'))
    perm.append(Permission.objects.get(name='Can delete match score'))
    perm.append(Permission.objects.get(name='Can change match score'))
    for p in perm:
        group.permissions.add(p)

    # Gets calendar data
    events = []
    for match in Match.objects.all():
        start = formats.date_format(match.date, "Y-m-d")
        end = formats.date_format(match.date, "Y-m-d")
        title = match.__str__()
        events.append([start, end, title, '#5f5f7b', '/jogos/' + str(match.id)])

    return render(request, 'home.html', {'events': json.dumps(events)})


def signup(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data[
                'email'], form.cleaned_data['password'])
            try:
                participant = Participant()
                participant.user = user
                participant.name = form.cleaned_data['name']
                participant.code = form.cleaned_data['code']
                participant.course = form.cleaned_data['course']
                participant.user.email = form.cleaned_data['email']
                participant.year = form.cleaned_data['year']
                user.save()
                participant.save()
                login_user(request, authenticate(username=form.cleaned_data[
                           'username'], password=form.cleaned_data['password']))
                messages.success(request, request, 'Cadastro realizado com sucesso.')
                return redirect('/')
            except:
                participant.delete()
                user.delete()
                messages.error(request, 'Não foi possível cadastrar o participante.')
                return render(request, 'signup.html', {'form': form, 'title': 'Cadastro de participante'}, status=400)
        return render(request, 'signup.html', {'form': form, 'title': 'Cadastro de participante'}, status=400)
    return render(request, 'signup.html', {'form': ParticipantForm(), 'title': 'Cadastro de participante'})


@login_required
def update_participant_info(request):
    participant = Participant.objects.get(user=request.user)
    initial = {'new_participant': 0, 'username': participant.user.username, 'name': participant.name, 'code': participant.code,
               'course': participant.course, 'email': participant.user.email, 'year': participant.year, 'old_email': participant.user.email}
    form = ParticipantForm(request.POST or None, initial=initial)
    form.fields['username'].widget = forms.HiddenInput()

    context = {
        'form': form,
        'action': '/meu-cadastro',
        'title': 'Alterar dados cadastrais',
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Meu cadastro'},
        ]
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                participant.name = form.cleaned_data['name']
                participant.code = form.cleaned_data['code']
                participant.course = form.cleaned_data['course']
                participant.user.email = form.cleaned_data['email']
                participant.year = form.cleaned_data['year']
                participant.user.set_password(form.cleaned_data['password'])
                participant.user.save()
                participant.save()
                login_user(request, authenticate(username=form.cleaned_data[
                           'username'], password=form.cleaned_data['password']))
                messages.success(request, request, 'Dados alterados com sucesso.')
                return render(request, 'signup.html', context)
            except:
                messages.error(request, 'Não foi possível alterar seus dados.')
                return render(request, 'signup.html', context, status=400)
        return render(request, 'signup.html', context, status=400)

    return render(request, 'signup.html', context)


def teams(request):
    context = {
        'title': 'Equipes',
        'teams': Team.objects.all(),
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Equipes'},
        ]
    }
    return render(request, 'teams.html', context)


@login_required()
def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            return redirect('/')
    else:
        form = TeamForm()

    context = {
        'title': "Nova Equipe",
        'action': '/equipes/nova',
        'cancel': '/',
        'form': form,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Equipes', 'link': '/'},
            {'name': 'Novo'},
        ]
    }
    return render(request, 'add-team.html', context)


@login_required()
def participant_filter(request):
    year = None
    max_number_of_teams = 3
    participants = []
    if request.method == 'GET':
        year = request.GET['year']
    if year != 'mix':
        participants = Participant.objects.filter(year=int(year))
    else:
        # generate random numbers different from each other
        random_numbers = set()
        while len(random_numbers) < max_number_of_teams:
            random_idx = random.randint(0, Participant.objects.count() - 1)
            random_numbers.add(random_idx)
        for i in range(0, max_number_of_teams):
            participants.append(Participant.objects.all()[random_numbers.pop()])
    participants_info = ""
    i = 1
    for participant in participants:
        participants_info += str(participant) + "," + str(participant.id)
        if i < len(participants):
            participants_info += "|"
        i = i + 1
    return HttpResponse(participants_info)


def login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login_user(request, user)
            return redirect(request.POST.get('next'))
        else:
            context['error'] = "Usuário ou senha inválidos."
            context['username'] = username

    return render(request, 'login.html', context)


def logout(request):
    logout_user(request)
    return redirect('/')


def about(request):
    return render(request, 'about.html')


@login_required
def validate_participants(request, participant_school):
    if request.method == 'POST':
        for participant in Participant.objects.filter(school=participant_school):
            p = request.POST.get(participant.user.username)
            if p == 'on':
                participant.valid = True
            else:
                participant.valid = False
            participant.save()

    participants = Participant.objects.filter(school=participant_school).order_by('name').all()
    return render(request, 'participants-validation.html', {'participants': participants})


def tournaments(request):
    context = {
        'title': 'Torneios',
        'tournaments': Tournament.objects.all(),
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios'},
        ]
    }
    return render(request, 'tournaments.html', context)


def edit_group(request):
    tournaments_id = 1
    competitions = Competition.objects.filter(tournament=tournaments_id)
    list_category = list(competitions.values_list('category', flat=True))
    thiscompetition = []
    array_team = []
    list_team = []
    depth = 0
    size_group = 3

    if request.method == 'POST':
        indexcategory = request.POST.getlist('categorys')
        if request.POST['action'] == 'Exibir' and indexcategory[0] != "-":
            thiscompetition = Competition.objects.filter(id=list_category[int(indexcategory[0]) - 1])
            this_competition = Competition.objects.get(id=list_category[int(indexcategory[0]) - 1])
            print(type(this_competition))
            list_team = Team.objects.all().filter(category=this_competition.category)
            # array_team = A list for support in handling items
            array_team = list(list_team.values_list('id', flat=True))

            # remove team that has a group
            for group in TeamGroup.objects.filter(competition=this_competition):
                for team in list_team:
                    if (group.teams.filter(id=team.id)):
                        array_team.remove(team.id)
            teamwithoutgroup = Team.objects.filter(pk__in=array_team)
            context = {
                'list_team': list_team, 'depth': depth,
                'teamwithoutgroup': teamwithoutgroup,
                'TeamGroups': TeamGroup.objects.filter(competition=this_competition),
                'competitions': competitions, 'category': this_competition.category.name
            }
            print(this_competition.category.name)
            return render(request, 'edit-group.html', context)

        # and not TeamGroup.objects.filter(competition=this_competition):
        if request.POST['action'] == 'Gerar chaveamento' and thiscompetition:
            i = 65
            TeamGroup.objects.filter(competition_category=thiscompetition.category.name).delete()
            while array_team:
                if(len(array_team) >= size_group):
                    # team_choices= Random elements of list support
                    team_choices = random.sample(list(array_team), size_group)
                else:
                    team_choices = random.sample(list(array_team), len(array_team))

                group = TeamGroup()
                group.depth = 0
                group.name = 'Chave ' + str(group.depth + 1) + chr(i)
                group.competition = thiscompetition
                group.save()
                for choice in team_choices:
                    group.teams.add(list_team.get(id=choice))
                    array_team.remove(choice)
                i = i + 1

            context = {
                'list_team': list_team, 'depth': depth,
                'Groups': TeamGroup.objects.filter(competition=thiscompetition), 'competitions': competitions
                #   ,'score_list':score_list
            }

            return render(request, 'edit-group.html', context)

    context = {
        'competitions': competitions, 'this_competition': thiscompetition}
    return render(request, 'edit-group.html', context)


def edit_team(request, equipe_id):
    team = get_object_or_404(Team, id=equipe_id)
    participants = Participant.objects.filter(team_participants=equipe_id)
    if request.method == 'POST':
        form = TeamForm(request.POST or None, instance=team)
        if form.has_changed():
            if not request.POST['participants']:
                form.participants = team.participants
                form.save()
            else:
                form.save()
    else:
        form = TeamForm(instance=team)

    context = {
        'title': "Editar Equipe",
        'action': '/equipes/editar/' + equipe_id,
        'cancel': '/',
        'form': form,
        'participants': participants,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Equipes', 'link': '/equipes'},
            {'name': team, 'link': '/equipes/' + equipe_id},
            {'name': 'Editar'},
        ]
    }

    return render(request, 'edit-team.html', context)


def rankings(request):
    context = {
        'title': 'Rankings e Estatísticas',
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Rankings'},
        ],
        "teste": 21
    }
    return render(request, 'rankings.html', context)


@login_required()
def add_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            return redirect('/torneios/' + str(tournament.id))
    else:
        form = TournamentForm()

    context = {
        'title': "Novo Torneio",
        'action': '/torneios/novo',
        'cancel': '/torneios',
        'form': form,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': 'Novo'},
        ]
    }

    return render(request, 'form.html', context)


def tournament_details(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    context = {
        'title': 'Torneio',
        'tournament': tournament,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': 'Torneio'},
        ]
    }

    return render(request, 'tournament-details.html', context)


@login_required()
def edit_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect('/torneios')
    else:
        form = TournamentForm(instance=tournament)

    context = {
        'title': "Editar Torneio",
        'action': '/torneios/editar/' + tournament_id,
        'cancel': '/torneios/' + tournament_id,
        'form': form,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': tournament, 'link': '/torneios/' + tournament_id},
            {'name': 'Editar'},
        ]
    }

    return render(request, 'form.html', context)


@login_required()
def remove_tournament(request, tournament_id):
    get_object_or_404(Tournament, id=tournament_id).delete()
    return redirect('/torneios')


@login_required()
def add_competition(request, tournament_id):
    if request.method == 'POST':
        form = CompetitionForm(request.POST, tournament_id)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.tournament = Tournament.objects.get(id=tournament_id)
            competition.save()
            return redirect('/competicoes/' + str(competition.id))

    else:
        form = CompetitionForm()

    tournament = get_object_or_404(Tournament, id=tournament_id)
    context = {
        'title': "Nova Competição",
        'action': '/competicoes/novo/' + tournament_id,
        'cancel': '/torneios/' + tournament_id,
        'form': form,
        'tournament': tournament,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': tournament, 'link': '/torneios/' + tournament_id},
            {'name': 'Competições', 'link': '/torneios/' + tournament_id},
            {'name': 'Nova'},
        ]
    }

    return render(request, 'form.html', context)


def competition_details(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    tournament = competition.tournament
    context = {
        'title': competition,
        'competition': competition,
        'tournament': tournament,
        'trials': competition.matchs.filter(intercampi=False),
        'intercampi': Match.objects.filter(competition=competition, intercampi=True).first(),
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': tournament, 'link': '/torneios/' + str(tournament.id)},
            {'name': "Competições", 'link': '/torneios/' + str(tournament.id)},
            {'name': competition.category},
        ]
    }

    return render(request, 'competition-details.html', context)


@login_required()
def add_match(request, competition_id):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.intercampi = request.POST['intercampi']
            match.competition = Competition.objects.get(id=competition_id)
            match.save()
            messages.success(request, 'Partida criada com sucesso.')
            return redirect('/competicoes/' + competition_id)
    else:
        form = MatchForm(initial={'date': '', 'start': '', 'end': ''})

    competition = get_object_or_404(Competition, id=competition_id)
    context = {
        'title': 'Nova Final' if request.GET.get('intercampi') else 'Nova Seletiva',
        'action': '/jogos/novo/' + competition_id,
        'cancel': '/competicoes/' + competition_id,
        'competition': competition,
        'form': form,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': competition.tournament, 'link': '/torneios/' + str(competition.tournament.id)},
            {'name': 'Competições', 'link': '/torneios'},
            {'name': competition, 'link': '/competicoes/' + str(competition.id)},
            {'name': 'Novo'},
        ]
    }

    return render(request, 'form.html', context)


def match_details(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    match_scores = MatchScore.objects.filter(match=match).order_by('-score').all()
    context = {
        'title': match.type() + ' - ' + str(match.competition),
        'match': match,
        'match_scores': match_scores,
        'responsible': match.responsible,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': match.competition.tournament, 'link': '/torneios/' +
             str(match.competition.tournament.id)},
            {'name': 'Competições', 'link': '/torneios'},
            {'name': match.competition, 'link': '/competicoes/' + str(match.competition.id)},
            {'name': match.type()},
        ]
    }

    return render(request, 'match-details.html', context)


@login_required()
def edit_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.user.username != match.responsible.username:
        return redirect('/')
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            messages.success(request, 'Partida editada com sucesso.')
            return redirect('/jogos/' + match_id)
    else:
        form = MatchForm(instance=match)

    competition = get_object_or_404(Competition, id=match.competition.id)
    context = {
        'title': "Editar " + match.type(),
        'action': '/competicoes/editar/' + match_id,
        'cancel': '/competicoes/' + match_id,
        'competition': competition,
        'form': form,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': match.competition.tournament, 'link': '/torneios/' +
             str(match.competition.tournament.id)},
            {'name': 'Competições', 'link': '/torneios'},
            {'name': match.competition, 'link': '/competicoes/' + str(match.competition.id)},
            {'name': match.type(), 'link': '/competicoes/' + str(match.id)},
            {'name': 'Editar'},
        ]
    }

    return render(request, 'form.html', context)


@login_required()
def remove_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.user.username != match.responsible.username:
        return redirect('/')
    competition_id = match.competition.id
    match.delete()
    messages.success(request, 'Partida removida com sucesso.')
    return redirect('/competicoes/' + str(competition_id))


def attend_to_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    competition = match.competition

    if request.method == 'POST':
        form = AttendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            email = form.cleaned_data['email']
            course = form.cleaned_data['course']
            participant = Participant.objects.create(name=name, code=code, email=email, course=course)
            MatchScore.objects.create(match=match, participant=participant)
            match.participants.add(participant)
            return redirect('/jogos/' + match_id)
    else:
        form = AttendForm()

    context = {
        'title': "Participar " + match.type(),
        'action': '/jogos/participar/' + match_id,
        'cancel': '/jogos/' + match_id,
        'competition': competition,
        'form': form,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': match.competition.tournament, 'link': '/torneios/' +
             str(match.competition.tournament.id)},
            {'name': 'Competições', 'link': '/torneios'},
            {'name': match.competition, 'link': '/competicoes/' + str(match.competition.id)},
            {'name': match.type(), 'link': '/jogos/' + str(match.id)},
            {'name': 'Participar'},
        ]
    }

    return render(request, 'form.html', context)


@login_required()
def leave_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    match.teams.remove(request.user)
    score = MatchScore.objects.get(match=match, participant=request.user)
    score.delete()
    return redirect('/jogos/' + str(match_id))


@login_required()
def update_score(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == 'POST':
        for score in match.scores.all():
            p = request.POST.getlist(str(score.id))
            score.pontos = p[0]
            score.tempo = p[1]
            score.save()

        messages.success(request, 'Pontuação atualizada com sucesso.')
        return redirect('/jogos/' + str(match_id))

    context = {
        'title': 'Atualizar Pontuação',
        'match': match,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': match.competition.tournament, 'link': '/torneios/' +
             str(match.competition.tournament.id)},
            {'name': 'Jogos', 'link': '/competicoes/' + str(match.competition.id)},
            {'name': 'Atualizar'},
        ]
    }

    return render(request, 'update-score.html', context)


def list_results(request):
    is_complete = False
    matches = Match.objects.all()

    for match in matches:
        matchScore = MatchScore.objects.all().filter(match=match)
        if match.teams.count() != matchScore.count():
            match.first_place = None
            match.save()
        elif match.teams.count() == matchScore.count() and match.first_place:
            is_complete = True

    context = {
        'title': 'Resultados',
        'matches': matches,
        'is_complete': is_complete,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Resultados'},
        ]
    }
    return render(request, 'list-results.html', context)


@login_required
@permission_required('website.add_matchscore', raise_exception=True)
def my_matches(request):
    if request.user.groups.all().filter(name='Judges'):
        match = Match.objects.all()
        text = "Setor de Juízes - Acesso a todas as partidas"
    else:
        match = Match.objects.all().filter(responsible=request.user)
        text = 'Minhas partidas (' + request.user.get_full_name() + ')'

    context = {
        'title': text,
        'ready_matches': Match.matches_ready_to_publish_result(match),
        'not_ready_matches': Match.match_not_ready(match),
        'already_published_matches': Match.match_already_published(match),
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Resultados', 'link': '/resultados'},
            {'name': 'Minhas partidas'},
        ]
    }

    return render(request, 'my-matches.html', context)


@login_required
def publish_result(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.user != match.responsible:
        return redirect('/resultados')
    match.first_place = MatchScore.objects.filter(match=match).order_by('-score').first().team
    match.save()
    return redirect('/minhas-partidas')


@login_required
@permission_required('website.add_matchscore', raise_exception=True)
def list_incomplete_scores(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if match.responsible != request.user:
        return HttpResponseForbidden('Somente o responsável pela partida pode pontuar equipes.')

    match_scores = MatchScore.objects.filter(match=match).order_by('-score').all()
    teams_incomplete_score = []

    for team in match.teams.all():
        if not MatchScore.objects.filter(team=team, match=match).exists():
            teams_incomplete_score.append(team)

    context = {
        'title': 'Definir pontuação da partida',
        'match': match,
        'match_scores': match_scores.order_by('-score'),
        'teams_without_match_score': teams_incomplete_score,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Torneios', 'link': '/torneios'},
            {'name': match.competition.tournament, 'link': '/torneios/' +
             str(match.competition.tournament.id)},
            {'name': 'Competições', 'link': '/torneios'},
            {'name': match.competition, 'link': '/competicoes/' + str(match.competition.id)},
            {'name': match.type(), 'link': '/jogos/' + str(match.id)},
            {'name': 'Definir pontuação'}
        ]
    }

    return render(request, 'matchscore-add.html', context)


@login_required
@permission_required('website.add_matchscore', raise_exception=True)
def add_matchScore(request, user_id, match_id, team_id):
    user = User.objects.all().filter(id=user_id).first()
    if request.user != user:
        return redirect('/resultados')
    match = get_object_or_404(Match, id=match_id)
    team = get_object_or_404(Team, id=team_id)
    competition = match.competition
    tournament = competition.tournament

    if request.method == 'POST':
        form = MatchScoreForm(request.POST)
        if form.is_valid():
            matchScore = form.save(commit=False)

            team.score = matchScore.score
            team.save()

            match.first_place = None
            match.save()

            matchScore.match = match
            matchScore.team = team
            matchScore.judge = user
            matchScore.date_time = datetime.now()
            matchScore.save()
            return redirect("/pontuacao/" + str(user_id) + '/' + str(match_id) + '/')
    else:
        form = MatchScoreForm()
        if not match.competition.category.need_time:
            form.disable('time')
        elif not match.competition.category.need_score:
            form.disable('score')

    context = {
        'title': "Pontuação - " + team.name,
        'action': '/pontuacao/' + str(user_id) + '/' + str(match_id) + '/' + str(team_id) + '/',
        'cancel': '/pontuacao/' + str(user_id) + '/' + str(match_id),
        'form': form,
        'competition': competition,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Resultados', 'link': '/resultados'},
            {'name': user.first_name, 'link': '/resultados/' + str(user_id)},
            {'name': 'Pontuação - ' + str(match), 'link': '/pontuacao/' + str(user_id) + '/' + str(match_id)},
            {'name': 'Nova'},
        ]
    }

    return render(request, 'form.html', context)


@login_required
@permission_required('website.change_matchscore', raise_exception=True)
def edit_match_score(request, match_id, match_score_id):
    match = get_object_or_404(Match, id=match_id)
    match_score = get_object_or_404(MatchScore, id=match_score_id)

    if request.user != match.responsible:
        HttpResponseForbidden()

    if request.method == 'POST':
        form = MatchScoreForm(request.POST, instance=match_score)
        if form.is_valid():
            match_score.match.first_place = None
            match_score.judge = request.user
            match_score.date_time = datetime.now()
            match_score.match.save()
            form.save()
            return redirect('/jogos/' + str(match_id) + '/pontuar')
    else:
        form = MatchScoreForm(instance=match_score)
        if not match_score.match.competition.category.need_time:
            form.disable('time')
        elif not match_score.match.competition.category.need_score:
            form.disable('score')

    context = {
        'title': "Pontuação - " + str(match_score.match) + ' - ' + match_score.team.name,
        'action': '/jogos/' + str(match_id) + '/pontuar/' + str(match_score_id) + '/',
        'cancel': '/jogos/' + str(match_id) + '/pontuar/',
        'form': form,
        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Resultados', 'link': '/resultados'},
            {'name': request.user.first_name, 'link': '/resultados/' + str(request.user.id)},
            {'name': 'Pontuação - ' + str(match_score.match), 'link': '/jogos/' + str(match_id) + '/pontuar'},
            {'name': 'Editar'},
        ]
    }

    return render(request, 'form.html', context)


@login_required
@permission_required('website.delete_matchscore', raise_exception=True)
def remove_match_score(request, match_id, match_score_id):
    match = get_object_or_404(Match, id=match_id)
    match_score = get_object_or_404(MatchScore, id=match_score_id)

    if request.user != match.responsible:
        return HttpResponseForbidden()

    match_id = match_score.match.id
    match_score.delete()
    return redirect('/jogos/' + str(match_id) + '/pontuar')
