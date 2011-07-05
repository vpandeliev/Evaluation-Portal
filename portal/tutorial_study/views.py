from django.http import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def stage_one(request):
    return render_to_response('tutorial_study/study_display.html', {'number': 1})


@login_required
def stage_two(request):
    return render_to_response('tutorial_study/study_display.html', {'number': 2})

