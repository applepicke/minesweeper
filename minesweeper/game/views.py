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
        'title': 'Minesweeper - ' + map.name,
        'name': map.name,
        'map': map.get_map_matrix('hidden')
    }

    return render(request, 'game.jade', data)

# Create a new game
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

# Check to see if a certain game exists
def check_game(request):
    name = request.GET.get('name')

    if Map.objects.filter(name=name).count() > 0:
        return HttpResponse('game-exists')

    return HttpResponse('game-doesnt-exist', status=400)

# Mark a position as revealed
# Sparks a chain reaction if player hit a super block
def mark(request, name):
    x = int(request.GET.get('x'))
    y = int(request.GET.get('y'))

    try:
        map = Map.objects.get(name=name)
    except Map.DoesNotExist:
        return HttpResponse('map-doesnt-exist', status=404)

    num_bombs = map.mark(x, y)
    win = map.check_for_win() and num_bombs != -1
    map.save()

    result = {}

    # User clicked on a bomb
    if num_bombs == -1:
        result['status'] = 'dead'
        result['map'] = map.get_map_matrix('reveal')
        map.delete()

    # Hit a regular space
    elif num_bombs > 0:
        result['status'] = 'clear'
        result['num_bombs'] = num_bombs

    # Hit a super space
    elif num_bombs == 0:
        result['status'] = 'superclear'
        result['num_bombs'] = num_bombs
        result['empties'] = map.compile_empties(x, y)
        map.save()

    if win:
        result['status'] = 'win'
        result['map'] = map.get_map_matrix('reveal')
        map.delete()

    return HttpResponse(json.dumps(result), mimetype='application/json')


