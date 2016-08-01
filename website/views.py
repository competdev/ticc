from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user

from .models import *
from .forms import *

def home(request):
	return render(request, 'home.html')

def login(request):
	context = {}

	if request.method == 'POST':
		matricula = request.POST['matricula']
		senha = request.POST['senha']
		user = authenticate(username=matricula, password=senha)
		if user is not None:
			login_user(request, user)
			return redirect(request.POST.get('next'))
		else:
			context['error'] = "Matrícula ou senha inválidos."
			context['matricula'] = request.POST['matricula']

	return render(request, 'login.html', context)

def logout(request):
	logout_user(request)
	return redirect('/')

def torneios(request):
	context = {
		'titulo': 'Torneios',
		'torneios': Torneio.objects.all(),
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios'},
		]
	}
	return render(request, 'torneios.html', context)

@permission_required('user.is_staff')
@login_required()
def torneios_novo(request):
	if request.method == 'POST':
		form = TorneioForm(request.POST)
		if form.is_valid():
			torneio = form.save()
			return redirect('/torneios/' + str(torneio.pk))
	else:
		form = TorneioForm()

	context = {
		'titulo': "Novo Torneio",
		'action': '/torneios/novo',
		'cancelar': '/torneios',
		'form': form,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': 'Novo'},
		]
	}

	return render(request, 'crud.html', context)

def torneios_detalhes(request, pkTorneio):
	torneio = get_object_or_404(Torneio, pk=pkTorneio)
	context = {
		'titulo': torneio,
		'torneio': torneio,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': torneio},
		]
	}

	return render(request, 'torneios-detalhes.html', context)

@permission_required('user.is_staff')
@login_required()
def torneios_editar(request, pkTorneio):
	torneio = get_object_or_404(Torneio, pk=pkTorneio)
	if request.method == 'POST':
		form = TorneioForm(request.POST, instance=torneio)
		if form.is_valid():
			form.save()
			return redirect('/torneios')
	else:
		form = TorneioForm(instance=torneio)

	context = {
		'titulo': "Editar Torneio",
		'action': '/torneios/editar/' + pkTorneio,
		'cancelar': '/torneios/' + pkTorneio,
		'form': form,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': torneio, 'link': '/torneios/' + pkTorneio},
			{'nome': 'Editar'},
		]
	}

	return render(request, 'crud.html', context)

@permission_required('user.is_staff')
@login_required()
def torneios_excluir(request, pkTorneio):
	get_object_or_404(Torneio, pk=pkTorneio).delete()
	return redirect('/torneios')

@permission_required('user.is_staff')
@login_required()
def competicoes_novo(request, pkTorneio):
	if request.method == 'POST':
		form = CompeticaoForm(request.POST, pkTorneio)
		if form.is_valid():
			competicao = form.save(commit=False)
			competicao.torneio = Torneio.objects.get(pk=pkTorneio)
			competicao.save()
			return redirect('/competicoes/' + str(competicao.pk))

	else:
		form = CompeticaoForm()

	torneio = get_object_or_404(Torneio, pk=pkTorneio)
	context = {
		'titulo': "Nova Competição",
		'action': '/competicoes/novo/' + pkTorneio,
		'cancelar': '/torneios/' + pkTorneio,
		'form': form,
		'torneio' : torneio,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': torneio, 'link': '/torneios/' + pkTorneio},
			{'nome': 'Competições', 'link': '/torneios/' + pkTorneio},
			{'nome': 'Nova'},
		]
	}

	return render(request, 'crud.html', context)

def competicoes_detalhes(request, pkCompeticao):
	competicao = get_object_or_404(Competicao, pk=pkCompeticao)
	torneio = competicao.torneio
	context = {
		'titulo': competicao,
		'competicao': competicao,
		'torneio': torneio,
		'seletivas': competicao.jogos.filter(intercampi=False),
		'intercampi': Jogo.objects.filter(competicao=competicao, intercampi=True).first(),
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': torneio, 'link': '/torneios/' + str(torneio.pk)},
			{'nome': "Competições", 'link': '/torneios/' + str(torneio.pk)},
			{'nome': competicao.categoria },
		]
	}

	return render(request, 'competicoes-detalhes.html', context)

@permission_required('user.is_staff')
@login_required()
def competicoes_editar(request, pkCompeticao):
	pass

@permission_required('user.is_staff')
@login_required()
def jogos_novo(request, pkCompeticao):
	if request.method == 'POST':
		form = JogoForm(request.POST)
		if form.is_valid():
			jogo = form.save(commit=False)
			jogo.intercampi = request.POST['intercampi']
			jogo.competicao = Competicao.objects.get(pk=pkCompeticao)
			jogo.save()
			return redirect('/competicoes/' + pkCompeticao)
	else:
		form = JogoForm()

	competicao = get_object_or_404(Competicao, pk=pkCompeticao)
	context = {
		'titulo': "Nova Seletiva",
		'action': '/jogos/novo/' + pkCompeticao,
		'cancelar': '/competicoes/' + pkCompeticao,
		'competicao': competicao,
		'form': form,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': competicao.torneio, 'link': '/torneios/' + str(competicao.torneio.pk)},
			{'nome': 'Competições', 'link': '/torneios'},
			{'nome': competicao, 'link': '/competicoes/' + str(competicao.pk)},
			{'nome': 'Editar'},
		]
	}

	return render(request, 'crud.html', context)

def jogos_detalhes(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)
	context = {
		'titulo': jogo.tipo(),
		'jogo': jogo,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': jogo.competicao.torneio, 'link': '/torneios/' + str(jogo.competicao.torneio.pk)},
			{'nome': 'Competições', 'link': '/torneios'},
			{'nome': jogo.competicao, 'link': '/competicoes/' + str(jogo.competicao.pk)},
			{'nome': jogo.tipo() },
		]
	}

	return render(request, 'jogos-detalhes.html', context)

@permission_required('user.is_staff')
@login_required()
def jogos_editar(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)
	if request.method == 'POST':
		form = JogoForm(request.POST, instance=jogo)
		if form.is_valid():
			form.save()
			return redirect('/jogos/' + pkJogo)
	else:
		form = JogoForm(instance=jogo)

	competicao = get_object_or_404(Competicao, pk=jogo.competicao.pk)
	context = {
		'titulo': "Editar " + jogo.tipo(),
		'action': '/jogos/editar/' + pkJogo,
		'cancelar': '/jogos/' + pkJogo,
		'competicao': competicao,
		'form': form,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': jogo.competicao.torneio, 'link': '/torneios/' + str(jogo.competicao.torneio.pk)},
			{'nome': 'Competições', 'link': '/torneios'},
			{'nome': jogo.competicao, 'link': '/competicoes/' + str(jogo.competicao.pk)},
			{'nome': jogo.tipo(), 'link': '/jogos/' + str(jogo.pk) },
			{'nome': 'Editar'},
		]
	}
	
	return render(request, 'crud.html', context)

@permission_required('user.is_staff')
@login_required()
def jogos_excluir(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)
	pkCompeticao = jogo.competicao.pk
	jogo.delete()
	return redirect('/competicoes/' + str(pkCompeticao))

@login_required()
def jogos_participar(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)
	jogo.participantes.add(request.user)
	Pontuacao.objects.create(jogo=jogo, participante=request.user)
	return redirect('/jogos/' + str(pkJogo))

@login_required()
def jogos_sair(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)
	jogo.participantes.remove(request.user)
	pontuacao = Pontuacao.objects.get(jogo=jogo, participante=request.user)
	pontuacao.delete()
	return redirect('/jogos/' + str(pkJogo))

@permission_required('user.is_staff')
@login_required()
def pontuacao_atualizar(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)

	if request.method == 'POST':
		for pontuacao in jogo.pontuacao.all():
			p = request.POST.getlist(str(pontuacao.pk))
			pontuacao.pontos = p[0]
			pontuacao.tempo = p[1]
			pontuacao.save()

		return redirect('/jogos/' + str(pkJogo))

	context = {
		'titulo': 'Atualizar Pontuação',
		'jogo': jogo,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': jogo.competicao.torneio, 'link': '/torneios/' + str(jogo.competicao.torneio.pk)},
			{'nome': 'Jogos', 'link': '/competicoes/' + str(jogo.competicao.pk)},
			{'nome': 'Atualizar'},
		]
	}

	return render(request, 'pontuacao-atualizar.html', context)	

