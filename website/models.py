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

class Participant(models.Model):
	#participant now have an user only for leader (when leader attr is True).
	user = models.ForeignKey(User, null=True)
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=12)
	email = models.EmailField(max_length=255)
	year = models.IntegerField(choices=((1,'1º'),(2,'2º'),(3,'3º')))
	school = models.CharField(max_length=255)
	course = models.CharField(max_length=255)
	valid = models.BooleanField(default=False)


	def __str__(self):
		return self.name + ' - ' + str(self.year) + 'º ano' + ' - ' + self.school 

class Team(models.Model):
	name = models.CharField(max_length=255)
	score = models.IntegerField(default=0)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	participants = models.ManyToManyField(Participant, related_name='team_participants')
	mix_team = models.BooleanField(default=False)

	def __str__(self):
		return self.name

#modelo chave:
class Group(models.Model):
	name = models.CharField(max_length=255)#the name pattern (A,B,C,1,2,3,etc) of a group needs to be choose by TICC's staff.
	depth = models.IntegerField(default=0)#the function of depth attr is to determine how close to the final match a grouṕ is.
	competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
	teams = models.ManyToManyField(Team, related_name='group_teams')

	def __str__(self):
		return self.name


class Match(models.Model):
	competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matchs')
	campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
	responsible = models.ForeignKey(User)
	date = models.DateField(default=date.today)
	start = models.TimeField(default=timezone.now)
	end = models.TimeField(default=timezone.now)
	location = models.CharField(max_length=255)
	teams = models.ManyToManyField(Team, related_name='teams')
	group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
	intercampi = models.BooleanField(default=False)
	first_place = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='first_place', blank=True, null=True)

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
			matchScore = MatchScore.objects.all().filter(match=match)
			if match.teams.count()==matchScore.count() and not match.first_place and matchScore.count()!=0:
				MATCHS.append(match)
		return MATCHS

	def match_not_ready(request):
		matchs = Match.objects.all().filter(responsible=request.user)
		MATCHS = []
		for match in matchs:
			matchScore = MatchScore.objects.all().filter(match=match)
			if match.teams.count()!=matchScore.count() or matchScore.count()==0:
				MATCHS.append(match)
		return MATCHS

	def match_already_published(request):
		matchs = Match.objects.all().filter(responsible=request.user)
		MATCHS = []
		for match in matchs:
			matchScore = MatchScore.objects.all().filter(match=match)
			if match.teams.count()==matchScore.count() and matchScore.count()!=0 and match.first_place:
				MATCHS.append(match)
		return MATCHS

class MatchScore(models.Model):
	match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='scores')
	team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
	score = models.IntegerField(default=0)
	time = models.TimeField(default='00:00')

	def __str__(self):
		return self.team.__str__() + ' - ' + self.match.__str__()
