from django.http import *
from django.shortcuts import render_to_response
from models import *
import random

# Create your views here.
def play_rushhour_game(request):
    """docstring for play"""

    return render_to_response('game.html')
    

def make_rushhour_game(request):
    """docstring for play"""
    return render_to_response('gamemaker.html')
    
def get_level(request):
    print "fuck you all"
    order = random.randint(1,10)
    print order
    level = Level.objects.get(order=order)

    return HttpResponse(level.content)

    