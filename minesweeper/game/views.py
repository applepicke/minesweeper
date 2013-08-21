from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from minesweeper.game.models import Map

# Create your views here.
def home(request):
    return render(request, 'home.jade', {})

def create_game(request):
    name = request.GET.get('name')

    # Check if game already exists
    if Map.objects.filter(name=name).count() > 0:
        return HttpResponse('game-exists')

    map = Map(
        name=name,
        width=settings.GAME_WIDTH,
        height=settings.GAME_HEIGHT,
        num_bombs=settings.NUM_BOMBS,
    )
    map.generate_map()
    print map.data

    return HttpResponse('hello')

def show_game(request, game):
    return HttpResponse(game)

def mark(request, game):
    return HttpResponse("mark" + game)