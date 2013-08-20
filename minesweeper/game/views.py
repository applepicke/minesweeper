from django.http import HttpResponse
from minesweeper.game.models import Map

# Create your views here.
def home(request):
    map = Map(data='BEBEEBEBE', width=3, height=3)
    print map.data
    map._change_contents(1, 0, 'H')
    print map.data


    return HttpResponse("Hello world.")


def showGame(request, game):
    return HttpResponse(game)

def mark(request, game):
    return HttpResponse("mark" + game)