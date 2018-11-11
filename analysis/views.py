from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import website
from website.models import Submission, Match
from django.db.models import Count
from django.db.models import F
from itertools import groupby
from math import ceil, trunc


submission_filters = (
    ('campus', 'team__members__campus_id'), 
    ('course', 'team__members__course_id'), 
    ('year', 'match__competition__tournament__year'), 
    ('team', 'team__id'), 
    ('participant', 'team__members__id'),
    ('match', 'match_id')
)

def get_filters(request, available_filters=submission_filters):

    filters = {}

    for name, lookup in available_filters:
        value = request.query_params.get(name)
        if value:
            try:
                filters[f'{lookup}__in'] = [int(v) for v in value.split(',')]
            except ValueError:
                raise ValidationError(dict(detail=f'Filtro "{name}" inválido.'))

    return filters


def get_problem_type_color(problem_type):
    return {
        2: '#f4a62a',
        3: '#58b120',
        4: '#e74c3c',
        5: '#8d816f',
        6: '#9b59b6',
        7: '#ef6ea3',
        8: '#34495e',
    }[problem_type]


def get_submission_status_color(submission_status):
    return {
        1: '#00aa00',
        2: '#fc3c3c',
        3: '#e6b125',
        4: '#00b0c9',
        5: '#828c3f',
        6: '#376ace',
        7: '#430064',
    }[submission_status]

class SolvedProblemView(APIView):
    
    def get(self, request):
        values = ('problem_type', )
        filters = get_filters(request)
        result = (Submission.objects
            .filter(status=1, **filters)
            .values(
                'problem_type__id',
                'problem_type__name', 
                'match__competition__tournament__year')
            .annotate(
                Count('match__competition__tournament__year'),
                value=Count('problem_type'))
            .order_by('-value')
            .all())

        data = []
        for r in result:
            d = dict(
                year=r['match__competition__tournament__year'],
                problem_type=r['problem_type__name'],
                value=r['value'],
                color=get_problem_type_color(r['problem_type__id'])
            )
            data.append(d)

        return Response(data)


class SubmissionsView(APIView):
    
    def get(self, request):
        values = ('problem_type', )
        filters = get_filters(request)
        result = (Submission.objects
            .filter(**filters)
            .values(
                'problem_type__name', 
                'match__competition__tournament__year',
                'status',
            )
            .annotate(
                Count('match__competition__tournament__year'),
                value=Count('problem_type'))
            .order_by('-value')
            .all())

        data = []
        for r in result:
            d = dict(
                year=r['match__competition__tournament__year'],
                problem_type=r['problem_type__name'],
                submission_acceptance='aceita' if r['status'] == 1 else 'rejeitada',
                submission_status=Submission.Status[r['status'] - 1][1],
                value=r['value'],
                color='#00aa00' if r['status'] == 1 else '#fc3c3c',
            )
            data.append(d)

        return Response(data)


class SubmissionErrorsView(APIView):
    
    def get(self, request):
        values = ('problem_type', )
        filters = get_filters(request)
        result = (Submission.objects
            .exclude(status=1)
            .filter(**filters)
            .values(
                'problem_type__name', 
                'match__competition__tournament__year',
                'status',
            )
            .annotate(
                Count('match__competition__tournament__year'),
                Count('status'),
                value=Count('problem_type'))
            .order_by('-value')
            .all())

        data = []
        for r in result:
            d = dict(
                year=r['match__competition__tournament__year'],
                problem_type=r['problem_type__name'],
                submission_status=Submission.Status[r['status'] - 1][1],
                value=r['value'],
                color=get_submission_status_color(r['status']),
            )
            data.append(d)

        return Response(data)


class FirstSubmissionView(APIView):
    
    def get(self, request):
        values = ('problem_type', )
        filters = get_filters(request)
        result = (Submission.objects
            .filter(**filters)
            .values(
                'problem_type__name', 
                'problem_type__id', 
                'match__competition__tournament__year',
                'status',
                'submitted_in',
                'team_id',
            )
            .annotate(
                Count('match__competition__tournament__year'),
                Count('status'),
                value=Count('problem_type'))
            .order_by('team_id', 'submitted_in')
            .all())

        data = []

        submissions_per_team = groupby(result, key=lambda x: x['team_id'])
        for team_id, submissions in submissions_per_team:
            r = [s for s in submissions][0]
            data.append(dict(
                year=r['match__competition__tournament__year'],
                problem_type=r['problem_type__name'],
                submission_acceptance='aceita' if r['status'] == 1 else 'rejeitada',
                submission_status=Submission.Status[r['status'] - 1][1],
                value=r['value'],
                submission_status_color=get_submission_status_color(r['status']),
                problem_type_color=get_problem_type_color(r['problem_type__id']),
                submission_acceptance_color='#00aa00' if r['status'] == 1 else '#fc3c3c',
            ))

        return Response(data)


class CardsView(APIView):
    
    match_available_filters = (
        ('campus', 'teams__members__campus_id'), 
        ('course', 'teams__members__course_id'), 
        ('year', 'competition__tournament__year'), 
        ('team', 'teams__id'), 
        ('participant', 'teams__members__id'),
        ('match', 'id'),
    )

    def get(self, request):
        query = Submission.objects.filter(**get_filters(request))
        submissions_count = query.count()
        solved_problems_count = query.filter(status=1).count()
        matches = Match.objects.filter(**get_filters(request, self.match_available_filters)).all()
        problems_count = 0
        for match in matches:
            teams_count = 0
            teams_query = match.teams
            team = request.query_params.get('team')
            participant = request.query_params.get('participant')
            if team:
                teams_query = teams_query.filter(pk=team)
            if participant:
                teams_query = teams_query.filter(members__pk=participant)
            problems_count += match.problem_types.count() * teams_query.count()
        problem_types = [x for x in query
            .filter(status=1)
            .values('problem_type__name')
            .annotate(value=Count('problem_type'))
            .order_by('value')
            .all()]
        most_common_error = (query
            .exclude(status=1)
            .values('status')
            .annotate(value=Count('status'))
            .order_by('-value')
            .first())
        most_common_error = dict(
            name=Submission.Status[most_common_error['status'] - 1][1],
            value=round(100 * most_common_error['value'] / submissions_count, 0) if submissions_count else 0
        ) if most_common_error else dict(name='-', value=0) 

        least_solved_problem_type = problem_types[0] if problem_types else dict(problem_type__name='-', value=0)
        most_solved_problem_type = problem_types[-1] if problem_types else dict(problem_type__name='-', value=0)
        accepted_submissions = round((100 * solved_problems_count / submissions_count) if submissions_count else 0, 0)
        solved_problems = round((100 * solved_problems_count / problems_count) if problems_count else 0, 0)

        return Response(dict(
            accepted_submissions=f'{accepted_submissions}%',
            solved_problems=f'{solved_problems}%',
            problems_count=problems_count,
            most_solved_problem_type=most_solved_problem_type,
            least_solved_problem_type=least_solved_problem_type,
            most_common_error=most_common_error,
        ))
