from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone

class Campus(models.Model):
	location = models.CharField(max_length=255)
	number = models.CharField(max_length=2)

	def __str__(self):
		return 'Campus ' + self.number + ' - ' + self.location

class Category(models.Model):
	name = models.CharField(max_length=255)
	rules = models.TextField()

	def __str__(self):
		return self.name

class Tournament(models.Model):
	location = models.ForeignKey(Campus, on_delete=models.CASCADE, default=None)
	responsible = models.ForeignKey(User)
	start = models.DateField()
	end = models.DateField()

	def status(self):
		now = date.today()
		if now < self.start:
			return 'status-waiting'
		elif now <= self.end:
			return 'status-in-progress'
		else:
			return 'status-ended'

	def __str__(self):
		return str(self.start.year)

class Competition(models.Model):
	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="competitions")
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.category.name

	def status(self):
		pass

class Participant(models.Model): #integrar com tabela equipe
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=12)
	email = models.EmailField(max_length=255)
	course = models.CharField(max_length=255)
	#adicionar User (pode ser nulo)

	def __str__(self):
		return self.name + ' - ' + self.course

class Match(models.Model):
	competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matches')
	campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
	responsible = models.ForeignKey(User)
	date = models.DateField(default=date.today)
	start = models.TimeField(default=timezone.now)
	end = models.TimeField(default=timezone.now)
	location = models.CharField(max_length=255)
	participants = models.ManyToManyField(Participant, related_name='participants') #mudar para equipe
	intercampi = models.BooleanField(default=False)
	first_place = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='first_place', null=True, blank=True)
	complete = models.BooleanField(default=False) 
	#Colocar restricao de equipes no formulario
	#Numero de MatchScores = Numero de Participantes -> True

	def status(self):
		now = datetime.now()
		start = datetime.combine(self.date, self.start)
		end = datetime.combine(self.date, self.end)
		if now < start:
			return 'status-waiting'
		elif now <= end:
			return 'status-in-progress'
		else:
			return 'status-ended'

	def type(self):
		if self.intercampi:
			return "Final"
		else:
			return "Seletiva"

	def __str__(self):
		return self.competition.category.name + ' (' + self.campus.__str__() + ')'

	def matchs_ready_to_publish_result(request):
		matchs = Match.objects.all().filter(responsible=request.user)
		MATCHS = []
		for match in matchs:
			if match.complete and not match.first_place:
				MATCHS.append(match)
		return MATCHS

	def match_not_ready(request):
		matchs = Match.objects.all().filter(responsible=request.user)
		MATCHS = []
		for match in matchs:
			matchScore = MatchScore.objects.all().filter(match=match)
			if not match.complete:
				MATCHS.append(match)
		return MATCHS

class MatchScore(models.Model):
	match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='scores')
	participant = models.ForeignKey(Participant, on_delete=models.CASCADE, null=True) #equipe
	score = models.IntegerField(default=0)
	time = models.IntegerField(default=0, blank=True)

	def __str__(self):
		return self.participant.name + ' - ' + self.match.__str__()
