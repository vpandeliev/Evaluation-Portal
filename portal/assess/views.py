# Create your views here.
from django.http import *
from django.shortcuts import render_to_response
from models import *
from portal.studies.models import *
import random, datetime
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

@login_required
def set_switch(request):
    """docstring for set_switch"""
    sid = request.session['study_id']
    study = Study.objects.get(id=sid)
    
    blocks = max(9 - study.assess_blocks, 1);
    trials = max(study.assess_trials, 5);
    return render_to_response('assess/setswitch.html', locals())

@login_required
def flanker(request):
    """docstring for set_switch"""
    sid = request.session['study_id']
    study = Study.objects.get(id=sid)
    
    blocks = max(9 - study.assess_blocks, 1);
    trials = max(study.assess_trials, 5);
    return render_to_response('assess/flanker.html', locals())
