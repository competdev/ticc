from django.db import models
from django.contrib.auth.models import User

class Campus(models.Model):
	cidade = models.CharField(max_length=255)
	numero = models.CharField(max_length=2)

	def __str__(self):
		return 'Campus ' + self.numero + ' - ' + self.cidade

class Categoria(models.Model):
	nome = models.CharField(max_length=255)
	regras = models.TextField()

class Torneio(models.Model):
	sede = models.ForeignKey(Campus, on_delete=models.CASCADE)
	responsavel = models.ForeignKey(User)
	data_inicio = models.DateField()
	data_termino = models.DateField()

	def status(self):
		pass

class Competicao(models.Model):
	torneio = models.ForeignKey(Torneio, on_delete=models.CASCADE)
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
	responsavel = models.ForeignKey(User)

	def status(self):
		pass

class Jogo(models.Model):
	competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE)
	campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
	responsavel = models.ForeignKey(User)
	data = models.DateTimeField()
	local = models.CharField(max_length=255)
	participantes = models.ManyToManyField(User, related_name='jogos')
	seletiva = models.BooleanField(default=False)

class Pontuacao(models.Model):
	competicao = models.ForeignKey(Competicao, on_delete=models.CASCADE)
	pontos = models.IntegerField(default=0)
	participante = models.ForeignKey(User)