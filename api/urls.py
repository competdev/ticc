from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


router = routers.SimpleRouter(trailing_slash=False)
router.register('participants', views.ParticipantView, base_name='participants')
router.register('teams', views.TeamView, base_name='teams')

urlpatterns = router.urls + [
    path('tournaments', views.TournamentView.as_view()),
    path('campi', views.CampusView.as_view()),
    path('courses', views.CourseView.as_view()),
    path('years', views.YearView.as_view()),
    path('categories', views.CategoryView.as_view()),
    path('problem_types', views.ProblemTypeView.as_view()),
    path('matches', views.MatchView.as_view()),
    path('submissions', views.SubmissionView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
