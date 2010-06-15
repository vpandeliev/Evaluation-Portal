from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect
from models import *
from forms import NewStudyForm
from django.contrib.auth.decorators import login_required
#from blank import Blank



############### Study
@login_required
def show_many_studies(request):
	if StudyUser.objects.count > 0:
		studies = [x.study for x in StudyUser.objects.filter(user=request.user)]
	else:
		studies = []
		
	return render_to_response('show_many_studies.html', locals(), context_instance=RequestContext(request))

@login_required
def show_one_study(request,study_id):
	study = Study.objects.get(id=study_id)
	return render_to_response('show_one_study.html',locals(), context_instance=RequestContext(request))
	
@login_required
def show_users_in_study(request,study_id):
	users = Study.objects.filter(id=study_id).users()
	return render_to_response('show_users.html', locals(), context_instance=RequestContext(request))

@login_required
def create_one_study(request):
	if request.method == 'POST':
		form = NewStudyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data

			s = Study.objects.create(
				name=cd['name'],
				start_date=cd['start_date'],
				end_date=cd['end_date'],
				started=cd['started'],
				description=cd['description'])
			s.create_study_user(request.user)
			return HttpResponseRedirect('/study/')
	else:
		#study = Blank()
		form = NewStudyForm()
	return render_to_response('new_study.html', locals(), context_instance=RequestContext(request))
		
@login_required		
def edit_one_study(request,study_id):
	"""docstring for edit_one_study"""
	if request.method == 'POST':
		pass #update
	else: #render the form
		study = Study.objects.get(id=study_id)
		form = NewStudyForm(instance=study)
		return render_to_response('edit_study.html',locals(), context_instance=RequestContext(request))

@login_required
def remove_one_study(request,study_id):
	"""docstring for remoe_one_study"""
	s = Study.objects.get(id=study_id)
	StudyUser.objects.filter(study=s).delete()
	
	s.delete()
	return HttpResponseRedirect('/study/')
	
############### StudyUser

def invite_user(request,study_id):
	pass
	
def remove_user(request,study_id,user_id):
	pass


