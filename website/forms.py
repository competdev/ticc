from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User, Group
from .models import *


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'rules', 'need_score', 'need_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}),
            'rules': forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}),
            'need_score': forms.CheckboxInput(attrs={'autocomplete': 'off', 'style': 'width: 25%;'}),
            'need_time': forms.CheckboxInput(attrs={'autocomplete': 'off', 'style': 'width: 25%;'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['name'].label = 'Nome'
        self.fields['rules'].label = 'Regras'
        self.fields['need_score'].label = 'Pontuação como critério de avaliação'
        self.fields['need_time'].label = 'Tempo como critério de avaliação'

    def clean_need_score(self):
        try:
            score = self.data['need_score']
        except MultiValueDictKeyError:
            score = False
        try:
            time = self.data['need_time']
        except MultiValueDictKeyError:
            time = False
        if score == False and time == False:
            raise forms.ValidationError('É preciso selecionar pelo menos um critério de avaliação para a categoria.')
        return True


class TournamentForm(ModelForm):

    class Meta:
        model = Tournament
        fields = ['location', 'responsible', 'start', 'end']
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsible': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'start': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date', 'autocomplete': 'off'}, format='%d/%m/%Y'),
            'end': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date', 'autocomplete': 'off'}, format='%d/%m/%Y'),
        }

    def __init__(self, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsible'].choices = [('', '---------')] + [(user.id, user.get_full_name())
                                                                    for user in users if user.get_full_name() and Group.objects.get(name='admin') in user.groups.all()]
        self.fields['location'].label = 'Sede'
        self.fields['responsible'].label = 'Responsável'
        self.fields['start'].label = 'Início'
        self.fields['end'].label = 'Término'

    def clean_end(self):
        start = self.cleaned_data['start']
        end = self.cleaned_data['end']
        if end < start:
            raise forms.ValidationError('A data de término não pode ser anterior à data de início.')
        return end


class CompetitionForm(ModelForm):

    class Meta:
        model = Competition
        fields = ['category', 'responsible']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsible': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'})
        }

    def clean_category(self):
        try:
            tournament_id = self.data['tournament_id']
            category_id = self.data['category']
            competition = Competition.objects.get(tournament__id=tournament_id, category__id=category_id)
            raise forms.ValidationError('Este torneio já possui uma competição desta categoria.')
        except ObjectDoesNotExist:
            return Category.objects.get(id=category_id)

    def __init__(self, *args, **kwargs):
        super(CompetitionForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsible'].choices = [('', '---------')] + [(user.id, user.get_full_name())
                                                                    for user in users if user.get_full_name() and Group.objects.get(name='admin') in user.groups.all()]
        self.fields['responsible'].label = 'Responsável'
        self.fields['category'].label = 'Categoria'


class MatchForm(ModelForm):

    class Meta:
        model = Match
        fields = ['campus', 'responsible', 'date', 'start', 'end', 'location', 'first_place', 'finished']
        widgets = {
            'campus': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsible': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date', 'autocomplete': 'off'}, format='%d/%m/%Y'),
            'start': forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time', 'autocomplete': 'off', 'placeholder': '07:30'}, format='%H:%M'),
            'end': forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time', 'autocomplete': 'off', 'placeholder': '18:00'}, format='%H:%M'),
            'location': forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off', 'placeholder': 'Sala 203 do prédio principal'}),
            'first_place': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'finished': forms.CheckboxInput(),
        }
        help_texts = {
            'finished': 'Ao finalizar uma partida, ela será exibida na aba de resultados. Você pode alterar este campo a qualquer momento.'
        }

    def clean_campus(self):
        campus = self.cleaned_data['campus']
        competition_id = self.data['competition_id']

        if self.data['intercampi'] == False:
            if not self.instance.id:
                if Match.objects.filter(intercampi=False, competition__id=competition_id, campus=campus):
                    raise forms.ValidationError('Este campus já possui uma seletiva')
            else:
                if Match.objects.filter(intercampi=False, competition__id=competition_id, campus=campus).exclude(id=self.instance.id):
                    raise forms.ValidationError('Este campus já possui uma seletiva')

        return campus

    def clean_end(self):
        start = self.data['start']
        end = self.data['end']
        if end < start:
            raise forms.ValidationError('O horário de término não pode ser anterior ao horário de início.')
        return end

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['responsible'].choices = [('', '---------')] + [(user.id, user.get_full_name())
                                                                    for user in User.objects.all() if user.get_full_name() and Group.objects.get(name='admin') in user.groups.all()]
        self.fields['responsible'].label = 'Responsável'
        self.fields['start'].label = 'Início'
        self.fields['end'].label = 'Término'
        self.fields['date'].label = 'Data'
        self.fields['location'].label = 'Localização'
        self.fields['first_place'].label = 'Primeiro lugar'
        self.fields['finished'].label = 'Finalizar partida'


class MatchScoreForm(ModelForm):

    class Meta:
        model = MatchScore
        fields = ['score', 'time']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off', 'min_value': 0}),
            'time':  forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time', 'autocomplete': 'off', 'min_value': 0}, format='%H:%M')
        }

    def __init__(self, *args, **kwargs):
        super(MatchScoreForm, self).__init__(*args, **kwargs)
        self.fields['score'].label = 'Pontuação'
        self.fields['time'].label = 'Tempo'

    def clean_score(self):
        score = self.cleaned_data['score']
        if score < 0:
            raise forms.ValidationError('A pontuação não pode ser negativa.')
        return score

    def disable(self, field):
        self.fields[field].widget = forms.HiddenInput()


class ParticipantForm(forms.Form):
    id = forms.CharField(
        label='Nº de Matrícula', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        label='Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(
        label='Nome completo', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repassword = forms.CharField(
        label='Confirmar senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    campus = forms.ChoiceField(
        label='Campus', widget=forms.Select(attrs={'class': 'form-control'}))
    year = forms.ChoiceField(
        label='Ano', widget=forms.Select(attrs={'class': 'form-control'}))
    course = forms.ChoiceField(
        label='Curso', widget=forms.Select(attrs={'class': 'form-control'}))
    new_participant = forms.IntegerField(widget=forms.HiddenInput(), initial=1)

    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.fields['campus'].choices = [('', '---------')] + [(campus.id, campus.__str__()) for campus in Campus.objects.all()]
        self.fields['course'].choices = [('', '---------')] + [(course.id, course.__str__()) for course in Course.objects.all()]
        self.fields['year'].choices = [('', '---------')] + [(year.id, year.__str__()) for year in Year.objects.all()]

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            if User.objects.filter(email=data).exists() and self.data['new_participant'] == 1:
                raise ValidationError('E-mail já cadastrado.')
        except KeyError:
            raise ValidationError('Algo deu errado ao salvar seu e-mail. Por favor, tente novamente.')
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists() and self.data['new_participant'] == 1:
            raise ValidationError('Usuário já cadastrado.')
        return data

    def clean_password(self):
        if self.cleaned_data['password'] != self.data['repassword']:
            raise ValidationError('As senhas não conferem.')
        return self.cleaned_data['password']


class TeamForm(ModelForm):

    class Meta:
        model = Team
        fields = ['name', 'category', 'members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}),
            'category': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 100%;', 'widget': 'select'}),
        }

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nome'
        self.fields['category'].label = 'Categoria'
        self.fields['members'].label = 'Participantes'


class SignupTeamsForm(ModelForm):

    class Meta:
        model = Match
        fields = ['teams']
        widgets = {
            'members': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 100%;', 'widget': 'select'}),
        }

        def __init__(self, *args, **kwargs):
            super(SignupTeamsForm, self).__init__(*args, **kwargs)
            self.fields['teams'].required = False
