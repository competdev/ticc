from django.core.management.base import BaseCommand
from django.utils import timezone
from website import models
from faker import Faker
from django.db import transaction
import random
from django.contrib.auth.models import User
import datetime
import random
from django.utils import timezone
from .create_match import create_match
import os
import yaml


class Command(BaseCommand):
    help = 'Creates a tournament and populates it with mock data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        user = User.objects.first()
        last_year_tournament = models.Tournament.objects.order_by('-year').first()
        tournament_year = last_year_tournament.year + 1 if last_year_tournament else 2016
        tournaments_count = models.Tournament.objects.count()

        tournament = models.Tournament.objects.create(
            location_id=1,
            start=f'{tournament_year}-08-01',
            end=f'{tournament_year}-08-31',
            responsible=user,
            year=tournament_year,
        )

        competition = models.Competition.objects.create(
            tournament=tournament,
            category_id=1,
            responsible=user,
        )

        campi = (models.Campus.objects
            .prefetch_related('courses', 'courses__years').all())
        participants = models.Participant.objects.all()

        fake = Faker('pt_BR')
        current_file_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_file_path, 'team_names.yaml'), 'r') as f:
            team_names = yaml.load(f.read())['names']

        submissions = []

        for campus in campi:
            for course in campus.courses.all():
                for year in course.years.all():
                    p = [x for x in participants if 
                        x.year_id == year.id and x.course_id == course.id and x.campus == campus]
                    p_count = len(p)
                    i = 0
                    teams = []
                    while i + 2 < p_count:
                        team_name = random.choice(team_names)
                        team_names.remove(team_name)
                        team = models.Team.objects.create(
                            category_id=1,
                            name=team_name,
                            year=tournament_year,
                        )
                        p1 = random.choice(p)
                        p.remove(p1)
                        p2 = random.choice(p)
                        p.remove(p2)
                        p3 = random.choice(p)
                        p.remove(p3)
                        team.members.set([p1, p2, p3])
                        teams.append(team)
                        i += 3

                    for _ in range(3):
                        _, s = create_match(
                            teams, tournaments_count, competition, campus, user, tournament_year)
                        submissions.extend(s)

        models.Submission.objects.bulk_create(submissions)
        print(f'Torneio {tournament_year} criado.')
