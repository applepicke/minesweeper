from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import simplejson as json
from django.conf import settings

from minesweeper.game.models import Map

def home(request):
    return render(request, 'home.jade', {})

def show_game(request, name):
    try:
        map = Map.objects.get(name=name)
    except Map.DoesNotExist:
        return redirect('/')

    data = {
        'width': map.width,
        'height': map.height,
        'name': map.name,
        'map': map.get_map_matrix()
    }

    return render(request, 'game.jade', data)


def create_game(request):
    name = request.GET.get('name')

    # Check if game already exists
    if Map.objects.filter(name=name).count() > 0:
        return HttpResponse('game-exists', status=400)

    map = Map(
        name=name,
        width=settings.GAME_WIDTH,
        height=settings.GAME_HEIGHT,
        num_bombs=settings.NUM_BOMBS,
    )
    map.generate_map()
    map.save()

    return HttpResponse('game-created')

def check_game(request):
    name = request.GET.get('name')

    if Map.objects.filter(name=name).count() > 0:
        return HttpResponse('game-exists')

    return HttpResponse('game-doesnt-exist', status=400)

def mark(request, name):
    x = int(request.GET.get('x'))
    y = int(request.GET.get('y'))

    try:
        map = Map.objects.get(name=name)
    except Map.DoesNotExist:
        return HttpResponse('map-doesnt-exist', status=404)

    num_bombs = map.mark(x, y)
    map.save()

    result = {}

    if num_bombs == -1:
        result['status'] = 'dead'

    elif num_bombs > 0:
        result['status'] = 'clear'
        result['num_bombs'] = num_bombs

    elif num_bombs == 0:
        result['status'] = 'superclear'
        result['num_bombs'] = num_bombs
        result['empties'] = map._get_adj_empties(x, y)

    return HttpResponse(json.dumps(result), mimetype='application/json')


