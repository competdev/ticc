from django.db import models


class SolvedProblem(models.Model):

    campus = models.CharField(max_length=1000)
    course = models.CharField(max_length=1000)
    ano = models.CharField(max_length=1000)
    ano = models.CharField(max_length=4)
    team = models.CharField(max_length=1000)
    participant = models.CharField(max_length=1000)
    value = models.IntegerField()
