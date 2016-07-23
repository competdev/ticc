from django import forms
from django.db import models
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ObjectDoesNotExist

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

    def __init__(self, *args, **kwargs):
        super(TorneioForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsavel'].choices = [('', '---------')] + [(user.pk, user.get_full_name()) for user in users]

    def clean_termino(self):
        inicio = self.cleaned_data['inicio']
        termino = self.cleaned_data['termino']
        if termino < inicio:
            raise forms.ValidationError('A data de término não pode ser antes da data de início.')
        return termino

class CompeticaoForm(ModelForm):
    class Meta:
        model = Competicao
        fields = ['categoria', 'responsavel']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsavel': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'})
        }

    def clean_categoria(self):
        try:
            pkTorneio = self.data['pkTorneio']
            pkCategoria = self.data['categoria']
            competicao = Competicao.objects.get(torneio__pk=pkTorneio, categoria__pk=pkCategoria)
            raise forms.ValidationError('Competição já existente.')
        except ObjectDoesNotExist:
            return Categoria.objects.get(pk=pkCategoria)

    def __init__(self, *args, **kwargs):
        super(CompeticaoForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsavel'].choices = [('', '---------')] + [(user.pk, user.get_full_name()) for user in users]

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

    def clean_termino(self):
        inicio = self.data['inicio']
        termino = self.data['termino']
        if termino < inicio:
            raise forms.ValidationError('O horário de término não pode ser antes do horário de início.')
        return termino

    def __init__(self, *args, **kwargs):
        super(JogoForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsavel'].choices = [('', '---------')] + [(user.pk, user.get_full_name()) for user in users]