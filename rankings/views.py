from django.shortcuts import render
from website.models import *
from collections import *

# Create your views here.

def statistics(request):
    matches = Match.objects.filter(finished=True)
    campis = Campus.objects.all()

    teams = [[],[],[]]

    medal_board = {}
    
    for match in matches:
        if match.competition.category.need_time:
            matchscore = MatchScore.objects.filter(match=match).order_by('-score','time')
            teams[0].append(matchscore[0].team)
            teams[1].append(matchscore[1].team)
            teams[2].append(matchscore[2].team)
        else:
            matchscore = MatchScore.objects.filter(match=match).order_by('-score')
            teams[0].append(matchscore[0].team)
            teams[1].append(matchscore[1].team)
            teams[2].append(matchscore[2].team)

    for campus in campis:
        medal_board[str(campus)] = [0,0,0,0]

    for i in range(len(teams)):
        for team in teams[i]:
            if(team.mix_team==False):
                if(i==0):
                    medal_board[str(team.members.first().campus)][0] = medal_board [str(team.members.first().campus)][0] + 1
                elif(i==1):
                    medal_board[str(team.members.first().campus)][1] = medal_board [str(team.members.first().campus)][1] + 1
                else:
                    medal_board[str(team.members.first().campus)][2] = medal_board [str(team.members.first().campus)][2] + 1
                medal_board[str(team.members.first().campus)][3] =  medal_board[str(team.members.first().campus)][0] + medal_board[str(team.members.first().campus)][1] + medal_board[str(team.members.first().campus)][2]

            else:
                for participant in team.members.all():
                    if(i==0):
                        medal_board[str(participant.campus[i])][0] = medal_board[str(participant.campus[i])][0] + 1
                    elif(i==1):
                        medal_board[str(participant.campus[i])][1] = medal_board[str(participant.campus[i])][1] + 1
                    else:
                        medal_board[str(participant.campus[i])][2] = medal_board[str(participant.campus[i])][2] + 1
                    medal_board[str(participant.campus[i])][3] =  medal_board[str(participant.campus[i])][0] + medal_board[str(team.members.first().campus)][1] + medal_board[str(team.members.first().campus)][2]


    medal_board = OrderedDict(sorted(medal_board.items(), key=lambda t: (t[1][0],t[1][1],t[1][2]), reverse=True))

    campus_key = medal_board.keys()
    campus_values = medal_board.values()
    tuples = zip(campus_key, campus_values)

    context = {
        'title': 'Quadro de Medalhas',
        'tuples': tuples,
        'campis': campis,

        'breadcrumb': [
            {'name': 'Início', 'link': '/'},
            {'name': 'Rankings'},
        ],
        "teste": 21
    }
    return render(request, 'rankings.html', context)
