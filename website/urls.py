from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home),
	url(r'login$', views.login),
	url(r'logout$', views.logout),
	url(r'sobre$',views.about),
	url(r'torneios$', views.tournaments),
	url(r'resultados/$', views.list_results),

	url(r'torneios/novo', views.add_tournament),
	url(r'torneios/(?P<tournament_id>[0-9]+)$', views.tournament_details),
	url(r'torneios/editar/(?P<tournament_id>[0-9]+)$', views.edit_tournament),
	url(r'torneios/excluir/(?P<tournament_id>[0-9]+)$', views.remove_tournament),

	url(r'competicoes/novo/(?P<tournament_id>[0-9]+)$', views.add_competition),
	url(r'competicoes/(?P<competition_id>[0-9]+)$', views.competition_details),
	url(r'competicoes/editar/(?P<competition_id>[0-9]+)$', views.edit_competition),
	
	url(r'jogos/(?P<match_id>[0-9]+)$', views.match_details),
	url(r'jogos/novo/(?P<competition_id>[0-9]+)$', views.add_match),
	url(r'jogos/editar/(?P<match_id>[0-9]+)$', views.edit_match),
	url(r'jogos/excluir/(?P<match_id>[0-9]+)$', views.remove_match),
	url(r'jogos/participar/(?P<match_id>[0-9]+)$', views.attend_to_match),
	url(r'jogos/sair/(?P<match_id>[0-9]+)$', views.leave_match),

<<<<<<< HEAD
	url(r'pontuacao/(?P<user_id>[0-9]+)/(?P<match_id>[0-9]+)/$', views.list_incomplete_scores),
	url(r'pontuacao/editar/(?P<user_id>[0-9]+)/(?P<matchScore_id>[0-9]+)/$', views.edit_matchScore),
	url(r'pontuacao/exclui/(?P<user_id>[0-9]+)/(?P<matchScore_id>[0-9]+)/$', views.remove_matchScore),
	url(r'pontuacao/(?P<user_id>[0-9]+)/(?P<match_id>[0-9]+)/(?P<team_id>[0-9]+)/$', views.add_matchScore),
=======
	url(r'pontuacao/(?P<user_name>[a-zA-Z0-9_]*)/(?P<match_id>[0-9]+)/$', views.list_incomplete_scores),
	url(r'pontuacao/editar/(?P<user_name>[a-zA-Z0-9_]*)/(?P<matchScore_id>[0-9]+)/$', views.edit_matchScore),
	url(r'pontuacao/exclui/(?P<user_name>[a-zA-Z0-9_]*)/(?P<matchScore_id>[0-9]+)/$', views.remove_matchScore),
	url(r'pontuacao/(?P<user_name>[a-zA-Z0-9_]*)/(?P<match_id>[0-9]+)/(?P<team_id>[0-9]+)/$', views.add_matchScore),
>>>>>>> 8272774608999d141ef238fa774d24010f25f181

	url(r'resultados/(?P<user_id>[0-9]+)/$', views.list_incomplete_or_not_plubished_results),
	url(r'resultados/(?P<user_id>[0-9]+)/(?P<match_id>[0-9]+)/$', views.match_score),
	url(r'resultados/publica/(?P<user_id>[0-9]+)/(?P<match_id>[0-9]+)/$', views.publish_result),
]
