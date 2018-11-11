from django_filters import rest_framework as filters
from django.db.models import Q
from . import models
import website


class SubmissionFilter(filters.FilterSet):
    participant = filters.NumberFilter(field_name='team__members__id', lookup_expr='exact')
    team = filters.NumberFilter(field_name='team_id', lookup_expr='exact')

    class Meta:
        model = website.models.Submission
        fields = ('participant', 'team')
