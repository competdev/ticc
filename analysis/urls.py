from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('solved-problems', views.SolvedProblemView.as_view()),
    path('submissions', views.SubmissionsView.as_view()),
    path('submission-errors', views.SubmissionErrorsView.as_view()),
    path('first-submission', views.FirstSubmissionView.as_view()),
    path('cards', views.CardsView.as_view()),
]
