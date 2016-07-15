from django import forms
from django.forms import ModelForm
from .models import *


class TorneioForm(ModelForm):
	class Meta:
		model = Torneio
		fields = ['sede', 'responsavel', 'inicio', 'termino']
		widgets = {
            'sede': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsavel': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'inicio': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date', 'data-provide': 'datepicker'}, format='%d/%m/%Y'),
            'termino': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date', 'data-provide': 'datepicker'}, format='%d/%m/%Y'),
        }

class CompeticaoForm(ModelForm):
	class Meta:
		model = Competicao
		fields = ['categoria', 'responsavel']
		widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsavel': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
        }

class JogoForm(ModelForm):
	class Meta:
		model = Jogo
		fields = ['campus', 'responsavel', 'inicio', 'termino', 'local']
		widgets = {
            'campus': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsavel': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'widget': 'datetime', 'data-provide': 'datetimepicker'}, format='%d/%m/%Y %-H:%M'),
            'termino': forms.DateTimeInput(attrs={'class': 'form-control', 'widget': 'datetime', 'data-provide': 'datetimepicker'}, format='%d/%m/%Y %-H:%M'),
            'local': forms.TextInput(attrs={'class': 'form-control', 'widget': 'input'}),
        }