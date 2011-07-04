from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def build_study(request):
    return render_to_response('study_builder/build_study.html')

