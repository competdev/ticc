from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('solved-problems', views.SolvedProblemView.as_view()),
]
