from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
import website
from . import serializers


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


class ParticipantView(ListAPIView):
    serializer_class = serializers.ParticipantSerializer
    queryset = website.models.Participant.objects.all()
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class TeamView(ListAPIView):
    serializer_class = serializers.TeamSerializer
    queryset = website.models.Team.objects.all()
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class ProblemTypeView(ListAPIView):
    serializer_class = serializers.ProblemTypeSerializer
    queryset = website.models.ProblemType.objects.all()


class MatchView(ListAPIView):
    serializer_class = serializers.MatchSerializer
    queryset = website.models.Match.objects.all()

