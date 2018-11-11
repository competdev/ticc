from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import Match, MatchScore, Team, Tournament, Submission
from django.db import transaction
from django.db.models import Sum


def calculate_match_scores(match):
    teams = match.teams.all()
    scores = []
    for team in teams:
        score = Submission.objects.filter(
            team=team, match=match).aggregate(Sum('score'))['score__sum'] or 0
        scores.append(MatchScore(
                match=match,
                team=team,
                score=score,
            ))
        team.score += score
        team.save()
    return scores


def update_placements():
    tournaments = Tournament.objects.all()
    for tournament in tournaments:
        teams = Team.objects.filter(year=tournament.year).order_by('score').all()
        for i, team in enumerate(teams):
            team.placement = i + 1
            team.save()


class Command(BaseCommand):
    help = 'Calculates scores'

    @transaction.atomic
    def handle(self, *args, **options):
        matches = Match.objects.prefetch_related('teams').all()
        submissions = Submission.objects.all()
        scores = []

        MatchScore.objects.all().delete()

        for match in matches:
           scores.extend(calculate_match_scores(match))

        update_placements()

        MatchScore.objects.bulk_create(scores)
        print('Pontuações calculadas.')
