from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('campi', views.CampusView.as_view()),
    path('courses', views.CourseView.as_view()),
    path('years', views.YearView.as_view()),
    path('categories', views.CategoryView.as_view()),
    path('participants', views.ParticipantView.as_view()),
    path('teams', views.TeamView.as_view()),
    path('problem_types', views.ProblemTypeView.as_view()),
    path('matches', views.MatchView.as_view()),
]
