from django.conf.urls import patterns, include, url
from minesweeper.game import views as game_views

urlpatterns = patterns('',
    url(r'^$', game_views.home),
    url(r'^games/(?P<game>\w+)/$', game_views.showGame),
    url(r'^games/(?P<game>\w+)/mark/$', game_views.mark)
)
