from django.core.management.base import BaseCommand
from django.utils import timezone
from website import models
from faker import Faker
from django.db import transaction
import random
from django.contrib.auth.models import User
import datetime

def _get_problem_type(problem_number):
    return [
        2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7
    ][problem_number]

class Command(BaseCommand):
    help = 'Creates a tournament and populates it with mock data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        user = User.objects.first()
        tournament_year = 2018

        tournament = models.Tournament.objects.create(
            location_id=1,
            start=f'{tournament_year}-08-01',
            end=f'{tournament_year}-08-31',
            responsible=user,
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

        submissions = []

        for campus in campi:
            for course in campus.courses.all():
                for year in course.years.all():
                    p = [x for x in participants if 
                        x.year_id == year.id and x.course_id == course.id]
                    p_count = len(p)
                    i = 0
                    teams = []
                    while i + 2 < p_count:
                        team = models.Team.objects.create(
                            category_id=1,
                            name=fake.company(),
                        )
                        team.members.set([
                            p[i], p[i + 1], p[i + 2]
                        ])
                        teams.append(team)
                        i += 2

                    match = models.Match.objects.create(
                        competition=competition,
                        campus=campus,
                        responsible=user,
                        date=f'{tournament_year}-08-02',
                        start='8:00',
                        end='12:00',
                        location=campus.location,
                        intercampi=False,
                        finished=True
                    )

                    prob_try_solve_problem = 0.7
                    prob_accepted_answer = 0.5
                    try_again_chance = 0.8
                    try_again_change_drop_rate = 0.1
                    wrong_answer_chance = 0.6
                    problems_count = 12

                    for team in teams:
                        for i in range(problems_count):
                            will_try_solve = random.random() <= prob_try_solve_problem
                            submission_status = None
                            if will_try_solve:
                                j = 0
                                while True:
                                    accepted_answer = random.random() <= prob_accepted_answer
                                    if accepted_answer:
                                        submission_status = 1
                                        break
                                    else:
                                        is_wrong_answer = random.random() <= wrong_answer_chance
                                        if is_wrong_answer:
                                            submission_status = 2
                                        else:
                                            submission_status = random.choice(range(3, 6))

                                    will_try_again = random.random() <= (try_again_chance - (try_again_change_drop_rate * j))
                                    j += 1
                                    if not will_try_again:
                                        break

                            if submission_status:
                                submissions.append(models.Submission(
                                    match=match,
                                    team=team,
                                    problem=i + 1,
                                    status=submission_status,
                                    problem_type_id=_get_problem_type(i),
                                    submitted_in=datetime.datetime.now(),
                                ))
                print(f'Campus {campus.number}/Curso {course.name}/Ano {year.name}')

        models.Submission.objects.bulk_create(submissions)
