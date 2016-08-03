from django import forms
from django.db import models
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from captcha.fields import ReCaptchaField

class TorneioForm(ModelForm):
    class Meta:
        model = Torneio
        fields = ['sede', 'responsavel', 'inicio', 'termino']
        widgets = {
            'sede': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsavel': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'inicio': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date', 'autocomplete': 'off'}, format='%d/%m/%Y'),
            'termino': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date', 'autocomplete': 'off'}, format='%d/%m/%Y'),
        }

    def __init__(self, *args, **kwargs):
        super(TorneioForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsavel'].choices = [('', '---------')] + [(user.pk, user.get_full_name()) for user in users]
        self.fields['responsavel'].label = 'Responsável'
        self.fields['inicio'].label = 'Início'
        self.fields['termino'].label = 'Término'

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
            raise forms.ValidationError('Este torneio já possui uma competição desta categoria.')
        except ObjectDoesNotExist:
            return Categoria.objects.get(pk=pkCategoria)

    def __init__(self, *args, **kwargs):
        super(CompeticaoForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsavel'].choices = [('', '---------')] + [(user.pk, user.get_full_name()) for user in users]
        self.fields['responsavel'].label = 'Responsável'

class JogoForm(ModelForm):
    class Meta:
        model = Jogo
        fields = ['campus', 'responsavel', 'data', 'inicio', 'termino', 'local']
        widgets = {
            'campus': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'responsavel': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;', 'widget': 'select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'widget': 'date', 'autocomplete': 'off'}, format='%d/%m/%Y'),
            'inicio': forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time', 'autocomplete': 'off'}, format='%H:%M'),
            'termino': forms.TimeInput(attrs={'class': 'form-control', 'widget': 'time', 'autocomplete': 'off'}, format='%H:%M'),
            'local': forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'})
        }

    def clean_campus(self):
        campus = self.cleaned_data['campus']
        pkCompeticao = self.data['pkCompeticao']
        if not self.instance.pk:
            if Jogo.objects.filter(intercampi=False, competicao__pk=pkCompeticao, campus=campus):
                raise forms.ValidationError('Este campus já possui uma seletiva')
        else:
            if Jogo.objects.filter(intercampi=False, competicao__pk=pkCompeticao, campus=campus).exclude(pk=self.instance.pk):
                raise forms.ValidationError('Este campus já possui uma seletiva')

        return campus

        
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
        self.fields['responsavel'].label = 'Responsável'
        self.fields['inicio'].label = 'Início'
        self.fields['termino'].label = 'Término'

class ParticiparForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}), label='Nome', max_length=255)
    matricula = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}), label='Matrícula', max_length=12)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}), label='E-mail', max_length=255)
    curso = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'widget': 'input', 'autocomplete': 'off'}), label='Curso', max_length=255)
    captcha = ReCaptchaField()
