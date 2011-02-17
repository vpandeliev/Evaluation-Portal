# Create your views here.
from django.http import *
from django.shortcuts import render_to_response
from models import *
from studies.models import *
import random, datetime
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

@login_required
def set_switch(request):
    """docstring for set_switch"""
    return render_to_response('setswitch.html')

@login_required
def ss_done(request):
    """docstring for set_switch"""
    return render_to_response('setswitchdone.html')