from django import forms
from django.db import models
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from captcha.fields import ReCaptchaField

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
        self.fields['responsible'].choices = [('', '---------')] + [(user.id, user.get_full_name()) for user in users]
        self.fields['location'].label = 'Sede'
        self.fields['responsible'].label = 'Responsável'
        self.fields['start'].label = 'Início'
        self.fields['end'].label = 'Término'

    def clean_end(self):
        start = self.cleaned_data['start']
        end = self.cleaned_data['end']
        if end < start:
            raise forms.ValidationError('A data de término não pode ser antes da data de início.')
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
            raise forms.ValidationError('Este torneio já possui uma competição desta category.')
        except ObjectDoesNotExist:
            return Category.objects.get(id=category_id)

    def __init__(self, *args, **kwargs):
        super(CompetitionForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsible'].choices = [('', '---------')] + [(user.id, user.get_full_name()) for user in users]
        self.fields['responsible'].label = 'Responsável'

class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ['campus', 'responsible', 'date', 'start', 'end', 'location']
        widgets = {
            'campus': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsible': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date', 'autocomplete': 'off'}, format='%d/%m/%Y'),
            'start': forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time', 'autocomplete': 'off'}, format='%H:%M'),
            'end': forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time', 'autocomplete': 'off'}, format='%H:%M'),
            'location': forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'})
        }

    def clean_campus(self):
        campus = self.cleaned_data['campus']
        competition_id = self.data['competition_id']
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
            raise forms.ValidationError('O horário de término não pode ser antes do horário de início.')
        return end

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsible'].choices = [('', '---------')] + [(user.id, user.get_full_name()) for user in users]
        self.fields['responsible'].label = 'Responsável'
        self.fields['start'].label = 'Início'
        self.fields['end'].label = 'Término'
        self.fields['date'].label = 'Data'
        self.fields['location'].label = 'Localização'

class AttendForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}), label='Nome', max_length=255)
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}), label='Matrícula', max_length=12)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}), label='E-mail', max_length=255)
    course = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}), label='Curso', max_length=255)
    captcha = ReCaptchaField()

class MatchScoreForm(ModelForm):
    class Meta:
        model = MatchScore
        fields = ['score', 'time']
        widgets = {
            'score': forms.NumberInput(attrs={'class':'form-control','widget': 'input', 'autocomplete':'off', 'min_value': 0}),
            'time':  forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time', 'autocomplete': 'off', 'min_value': 0}, format='%H:%M')
        }

    def __init__(self, *args, **kwargs):
        super(MatchScoreForm, self).__init__(*args, **kwargs)
        self.fields['score'].label='Pontuação'
        self.fields['time'].label='Tempo'

    def clean_score(self):
        score = self.cleaned_data['score']
        if score < 0:
            raise forms.ValidationError('A pontuação não pode ser negativa')
        return score