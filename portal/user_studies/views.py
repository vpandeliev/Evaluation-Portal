
from django.http import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def welcome_page(request):
    return render_to_response('example_study/welcome_page.html')


@login_required
def simple_task(request):
    return render_to_response('example_study/simple_task.html')


@login_required
def bye_page(request):
    return render_to_response('example_study/bye_page.html')

