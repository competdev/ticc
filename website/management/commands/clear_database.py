from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from website import models
from django.db import transaction


class Command(BaseCommand):
    help = 'Clear database without dropping the schema'

    @transaction.atomic
    def handle(self, *args, **options):
        models.MatchScore.objects.all().delete()
        models.Submission.objects.all().delete()
        models.Match.objects.all().delete()
        models.Team.objects.all().delete()
        models.TeamGroup.objects.all().delete()
        models.Participant.objects.all().delete()
        models.Campus.objects.all().delete()
        models.Course.objects.all().delete()
        models.Year.objects.all().delete()
        models.Category.objects.all().delete()
        models.Tournament.objects.all().delete()
        models.Competition.objects.all().delete()
        models.ProblemType.objects.all().delete()
        User.objects.filter(is_superuser=False).all().delete()
