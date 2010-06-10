from django.shortcuts import render_to_response
from models import *

############### Study

def show_many_studies(request):
	studies = [x.study for x in StudyUser.objects.filter(user=request.user)]
	return render_to_response('study/show_many_studies.html', locals())

def show_one_study(request):
	pass



############### StudyUser
