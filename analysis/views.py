from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import website
from website.models import Submission
from django.db.models import Count
from django.db.models import F


class SolvedProblemView(APIView):
    
    def get(self, request):
        values = ('problem_type', )

        available_filters = (
            ('campus', 'team__members__campus_id'), 
            ('course', 'team__members__course_id'), 
            ('year', 'match__competition__tournament__year'), 
            ('team', 'team__id'), 
            ('participant', 'team__members__id'),
         )

        filters = {}

        for name, lookup in available_filters:
            value = request.query_params.get(name)
            if value:
                try:
                    filters[f'{lookup}__in'] = [int(v) for v in value.split(',')]
                except ValueError:
                    raise ValidationError(dict(detail=f'Filtro "{name}" inválido.'))

        result = (Submission.objects
            .filter(status=1, **filters)
            .values(
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
            )
            data.append(d)

        return Response(data)