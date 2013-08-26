from django.conf.urls import patterns, include, url
from minesweeper.game import views as game_views

urlpatterns = patterns('',
    url(r'^$', game_views.home),
    url(r'^create_game/$', game_views.create_game),
    url(r'^check_game/$', game_views.check_game),
    url(r'^games/(?P<name>(\w| )+)/$', game_views.show_game),
    url(r'^games/(?P<name>(\w| )+)/mark/$', game_views.mark),
)
