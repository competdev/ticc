from django.utils import timezone
from website import models
from faker import Faker
from django.db import transaction
import random
from django.contrib.auth.models import User
import datetime
import random
from django.utils import timezone


def _get_problem_type(problem_number):
    return [
        2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7
    ][problem_number]


def _get_problem_chance_of_solving(problem_type):
    return {
        2: 0.5,
        3: 0.4,
        4: 0.3,
        5: 0.2,
        6: 0.1,
        7: 0.05,
        8: 0.1
    }[problem_type]


def create_match(teams, tournaments_count, competition, campus, user, tournament_year):
    submissions = []
    match = models.Match.objects.create(
        competition=competition,
        campus=campus,
        responsible=user,
        date=f'{tournament_year}-08-02',
        start='8:00',
        end='12:00',
        intercampi=False,
        finished=True
    )
    match_duration = 4 * 60
    match.teams.set(teams)

    match_problem_types = []
    for k, problem_type_id in enumerate([2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]):
        match_problem_types.append(models.MatchProblemType(
            problem_type_id=problem_type_id,
            match=match,
            position=k + 1,
        ))

    models.MatchProblemType.objects.bulk_create(match_problem_types)

    prob_try_solve_problem = 0.7
    prob_accepted_answer = 0.4
    try_again_chance = 1
    try_again_change_drop_rate = 0.1
    wrong_answer_chance = 0.6
    problems_count = 12

    for team in teams:
        for i in range(problems_count):
            will_try_solve = random.random() <= prob_try_solve_problem
            problem_type = _get_problem_type(i)
            submission_status = None
            solving_time = random.randint(0, match_duration - 15)
            if will_try_solve:
                j = 0
                while submission_status != 1:
                    chance_of_solving = _get_problem_chance_of_solving(problem_type) + 1.5 * tournaments_count / 10
                    accepted_answer = random.random() <= chance_of_solving
                    if accepted_answer:
                        submission_status = 1
                    else:
                        is_wrong_answer = random.random() <= wrong_answer_chance
                        if is_wrong_answer:
                            submission_status = 2
                        else:
                            submission_status = random.choice(range(3, 6))

                    submissions.append(models.Submission(
                        match=match,
                        team=team,
                        problem=i + 1,
                        status=submission_status,
                        problem_type_id=problem_type,
                        submitted_in=timezone.now(),
                        score=(match_duration + match_duration - solving_time) if submission_status == 1 else 0,
                    ))

                    will_try_again = random.random() <= (try_again_chance - (try_again_change_drop_rate * j))
                    solving_time += 15
                    j += 1
                    if not will_try_again:
                        break

    return match, submissions
