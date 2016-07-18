from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from .forms import *

def home(request):
	return render(request, 'home.html')

def torneios(request):
	context = {
		'torneios': Torneio.objects.all(),
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios'},
		]
	}
	return render(request, 'torneios.html', context)

def torneios_novo(request):
	if request.method == 'POST':
		form = TorneioForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/torneios')
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
		'torneio': torneio,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': torneio},
		]
	}

	return render(request, 'torneios-detalhes.html', context)

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

def torneios_excluir(request, pkTorneio):
	get_object_or_404(Torneio, pk=pkTorneio).delete()
	return redirect('/torneios')


def competicoes_novo(request, pkTorneio):
	if request.method == 'POST':
		form = CompeticaoForm(request.POST)
		if form.is_valid():
			competicao = form.save(commit=False)
			competicao.torneio = Torneio.objects.get(pk=pkTorneio)
			competicao.save()
			return redirect('torneios/' + str(pkTorneio))
	else:
		form = CompeticaoForm()

	torneio = get_object_or_404(Torneio, pk=pkTorneio)
	context = {
		'titulo': "Nova Competicao",
		'action': '/competicoes/novo/' + pkTorneio,
		'cancelar': '/torneio/' + pkTorneio,
		'form': form,
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
		'competicao': competicao,
		'torneio': torneio,
		'seletivas': competicao.jogos.filter(intercampi=False),
		'intercampi': Jogo.objects.get(competicao=competicao, intercampi=True),
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': torneio, 'link': '/torneios/' + str(torneio.pk)},
			{'nome': "Competições", 'link': '/torneios/' + str(torneio.pk)},
			{'nome': competicao.categoria },
		]
	}

	return render(request, 'competicoes-detalhes.html', context)

def competicoes_editar(request, pkCompeticao):
	pass


def jogos_novo(request, pkCompeticao):
	if request.method == 'POST':
		form = JogoForm(request.POST)
		if form.is_valid():
			jogo = form.save(commit=False)
			jogo.competicao = Competicao.objects.get(pk=pkCompeticao)
			jogo.save()
			return redirect('/competicoes/' + pkCompeticao)
	else:
		form = JogoForm()

	competicao = get_object_or_404(Competicao, pk=pkCompeticao)
	context = {
		'titulo': "Novo Seletiva",
		'action': '/jogos/novo/' + pkCompeticao,
		'cancelar': '/competicoes/' + pkCompeticao,
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
	context = {
		'jogo': get_object_or_404(Jogo, pk=pkJogo),
	}

	return render(request, 'jogos-detalhes.html', context)

def jogos_editar(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)
	if request.method == 'POST':
		form = JogoForm(request.POST, instance=jogo)
		if form.is_valid():
			form.save()
			return redirect('/jogos/' + pkJogo)
	else:
		form = JogoForm(instance=jogo)

	context = {
		'titulo': "Editar Jogo",
		'action': '/jogos/editar/' + pkJogo,
		'cancelar': '/jogos/' + pkJogo,
		'form': form,
		'breadcrumb': [
			{'nome': 'Inicio', 'link': '/'},
			{'nome': 'Torneios', 'link': '/torneios'},
			{'nome': jogo.competicao.torneio, 'link': '/torneios/' + str(jogo.competicao.torneio.pk)},
			{'nome': 'Jogos', 'link': '/competicoes/' + str(jogo.competicao.pk)},
			{'nome': 'Editar'},
		]
	}
	
	return render(request, 'crud.html', context)

def jogos_excluir(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)
	pkCompeticao = jogo.competicao.pk
	jogo.delete()
	return redirect('/competicoes/' + str(pkCompeticao))

def jogos_participar(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)
	jogo.participantes.add(request.user)
	Pontuacao.objects.create(jogo=jogo, participante=request.user)
	return redirect('/jogos/' + str(pkJogo))

def jogos_sair(request, pkJogo):
	jogo = get_object_or_404(Jogo, pk=pkJogo)
	jogo.participantes.remove(request.user)
	pontuacao = Pontuacao.objects.get(jogo=jogo, participante=request.user)
	pontuacao.delete()
	return redirect('/jogos/' + str(pkJogo))
