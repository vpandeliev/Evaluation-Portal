from django.http import *
from django.shortcuts import render_to_response
from models import *
from studies.models import *
import random, datetime
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def play_rushhour_game(request):
    """docstring for play"""
    study_id = request.session['study_id']
    study = Study.objects.get(id=study_id)
    sp = study.get_study_participant(request.user)
    stage = sp.get_current_stage()
    #compare current time to timeout
    elapsed = datetime.datetime.now() - stage.curr_session_started
    if elapsed > datetime.timedelta(minutes=3):
        pass
        #return HttpResponseBadRequest()
    obj = Data.objects.filter(code='RSH', studyparticipant=sp)
    max = 0
    for a in obj:
        curr = int(a.datum.split(',')[0])
        if curr > max:
            max = curr
    
    order = max + 1
    level = Level.objects.get(order=order)

    reply = simplejson.dumps({'level':order, 'content': level.content})
    return render_to_response('game.html', {'level': level, 'content': reply, 'moves': level.moves})
    


def make_rushhour_game(request):
    """docstring for play"""
    return render_to_response('gamemaker.html')
    

def get_level(request):
    pass
'''    sp = StudyParticipant.objects.get(user=request.user)
    obj = Data.objects.filter(code='RSH', studyparticipant=sp)
    max = 0
    for a in obj:
        curr = int(a.datum.split(',')[0])
        if curr > max:
            max = curr
    
    order = max + 1
    level = Level.objects.get(order=order)

    reply = {'level':order, 'content': level.content}
    return HttpResponse(simplejson.dumps(reply))'''

    