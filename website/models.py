from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone

class Campus(models.Model):
	cidade = models.CharField(max_length=255)
	numero = models.CharField(max_length=2)

	def __str__(self):
		return 'Campus ' + self.numero + ' - ' + self.cidade

class Categoria(models.Model):
	nome = models.CharField(max_length=255)
	regras = models.TextField()

	def __str__(self):
		return self.nome

class Torneio(models.Model):
	sede = models.ForeignKey(Campus, on_delete=models.CASCADE, default=None)
	responsavel = models.ForeignKey(User)
	inicio = models.DateField()
	termino = models.DateField()

	def status(self):
		now = date.today()
		if now < self.inicio:
			return 'status-waiting'
		elif now <= self.termino:
			return 'status-in-progress'
		else:
			return 'status-ended'

	def __str__(self):
		return str(self.inicio.year)

class Competicao(models.Model):
	torneio = models.ForeignKey(Torneio, on_delete=models.CASCADE, related_name="competicoes")
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
	responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.categoria.nome

	def status(self):
		pass

class Jogo(models.Model):
	competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE, related_name="jogos")
	campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
	responsavel = models.ForeignKey(User)
	inicio = models.DateTimeField()
	termino = models.DateTimeField()
	local = models.CharField(max_length=255)
	participantes = models.ManyToManyField(User, related_name='jogos')
	intercampi = models.BooleanField(default=False)

	def status(self):
		now = timezone.now()
		if now < self.inicio:
			return 'status-waiting'
		elif now <= self.termino:
			return 'status-in-progress'
		else:
			return 'status-ended'

	def __str__(self):
		return self.campus.__str__()

class Pontuacao(models.Model):
	jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name="pontuacao")
	pontos = models.IntegerField(default=0)
	participante = models.ForeignKey(User)
