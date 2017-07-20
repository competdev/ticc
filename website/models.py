from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone


class Campus(models.Model):

    class Meta:
        verbose_name_plural = 'Campi'
	
    location = models.CharField(max_length=255)
    number = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return 'Campus ' + self.number + ' - ' + self.location


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Year(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    rules = models.TextField()
    need_score = models.BooleanField(default=False)
    need_time = models.BooleanField(default=False)
    final_only = models.BooleanField(default=False)
    icon = models.CharField(default='trophy', max_length=32)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    location = models.ForeignKey(Campus, on_delete=models.CASCADE, default=None, null=True)
    responsible = models.ForeignKey(User, null=True)
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

    def year(self):
        return self.start.year

    def verbose_status(self):
        if self.status() == 'status-waiting':
            return 'Não iniciada'
        if self.status() == 'status-in-progress':
            return 'Em progresso'
        return 'Finalizada'


class Competition(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="competitions", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.category.name


class Participant(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    valid = models.BooleanField(default=False)
    year = models.ForeignKey(Year)
    course = models.ForeignKey(Course)
    campus = models.ForeignKey(Campus)

    def __str__(self):
        return self.name + ' - ' + str(self.year) + 'º ano' + ' - ' + str(self.campus)


class Team(models.Model):
    name = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(Participant, related_name='teams')
    mix_team = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' id = ' + str(self.id)

    def str_members(self):
        return ', '.join([p.name for p in self.members.all()])


class TeamGroup(models.Model):
    name = models.CharField(max_length=255)
    depth = models.IntegerField(default=0)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team, related_name='groups')

    def __str__(self):
        return self.name


class Match(models.Model):

    class Meta:
        verbose_name_plural = 'Matches'

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matches', null=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, null=True)
    responsible = models.ForeignKey(User, null=True)
    date = models.DateField(default=date.today)
    start = models.TimeField(default=timezone.now)
    end = models.TimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    teams = models.ManyToManyField(Team, related_name='matches', blank=True)
    intercampi = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    first_place = models.ForeignKey(Team, blank=True, null=True)
    group = models.ForeignKey(TeamGroup, on_delete=models.CASCADE, null=True)

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

    def verbose_status(self):
        if self.status() == 'status-waiting':
            return 'Não iniciada'
        if self.status() == 'status-in-progress':
            return 'Em progresso'
        return 'Finalizada'

    def type(self):
        if self.intercampi:
            return "Final"
        else:
            return "Seletiva"

    def __str__(self):
        return self.competition.category.name + ' (' + self.campus.__str__() + ') - ' + self.type()


class MatchScore(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='scores')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default=0, blank=True, null=True)
    time = models.IntegerField(default=0, blank=True, null=True)
    judge = models.ForeignKey(User, null=True)
    date_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.team.__str__() + ' - ' + self.match.__str__()
