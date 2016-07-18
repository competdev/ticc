from django import forms
from django.db import models
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
        fields = ['campus', 'responsavel', 'data', 'inicio', 'termino', 'local']
        widgets = {
            'campus': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsavel': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date'}),
            'inicio': forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time'}),
            'termino': forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'widget': 'input'})
        }
