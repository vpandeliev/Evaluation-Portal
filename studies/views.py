from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import *
from forms import NewStudyForm

############### Study
#@logged_in
def show_many_studies(request):
	if StudyUser.objects.count > 0:
		studies = [x.study for x in StudyUser.objects.filter(user=request.user)]
	else:
		studies = []
	return render_to_response('show_many_studies.html', locals())

def show_one_study(request):
	pass

def show_users(request,study_id):
	users = Study.objects.filter(id=study_id).users()
	return render_to_response('show_users.html', locals())

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
			return HttpResponseRedirect('/thanks')
	else:
		form = NewStudyForm()
	return render_to_response('new_study.html', {'form': form})
		
		
def edit_one_study(request,study_id):
	"""docstring for edit_one_study"""
	if request.method == 'POST':
		pass #update
	else: #render the form
		pass

def remove_one_study(request,study_id):
	"""docstring for remoe_one_study"""
	pass
	
	
############### StudyUser

def invite_user(request,study_id):
	pass
	
def remove_user(request,study_id,user_id):
	pass


