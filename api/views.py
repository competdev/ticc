from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import website
from . import serializers, filters


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class TournamentView(ListAPIView):
    serializer_class = serializers.TournamentSerializer
    queryset = website.models.Tournament.objects.all()


class CampusView(ListAPIView):
    serializer_class = serializers.CampusSerializer
    queryset = website.models.Campus.objects.all()


class CourseView(ListAPIView):
    serializer_class = serializers.CourseSerializer
    queryset = website.models.Course.objects.all()


class YearView(ListAPIView):
    serializer_class = serializers.YearSerializer
    queryset = website.models.Year.objects.all()


class CategoryView(ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = website.models.Category.objects.all()


class ParticipantView(ModelViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.ParticipantSerializer
    queryset = website.models.Participant.objects.select_related('campus', 'year', 'course').all()
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class TeamView(ModelViewSet):
    serializer_class = serializers.TeamSerializer
    queryset = website.models.Team.objects.prefetch_related('members').all()
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['name']
    filter_fields = ['members__id']


class ProblemTypeView(ListAPIView):
    serializer_class = serializers.ProblemTypeSerializer
    queryset = website.models.ProblemType.objects.all()


class MatchView(ListAPIView):
    serializer_class = serializers.MatchSerializer
    queryset = website.models.Match.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id']


class SubmissionView(ListAPIView):
    serializer_class = serializers.SubmissionSerializer
    queryset = website.models.Submission.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = filters.SubmissionFilter
