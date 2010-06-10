from django.shortcuts import render_to_response
from models import *

############### Study
#@logged_in
def show_many_studies(request):
	studies = [x.study for x in StudyUser.objects.filter(user=request.user)]
	return render_to_response('study/show_many_studies.html', locals())

def show_one_study(request):
	pass

def show_users(request,study_id):
	users = Study.objects.filter(id=study_id).users()
	return render_to_response('study/show_users.html', locals())

def create_one_study(reqest):
	if request.method == 'POST':
		pass #create new
	else: #render the form
		pass
		
def edit_one_study(request,study_id):
	"""docstring for edit_one_study"""
	if request.method == 'POST':
		pass #update
	else: #render the form
		pass

def remoe_one_study(request,study_id):
	"""docstring for remoe_one_study"""
	pass
	
	
############### StudyUser

def invite_user(request,study_id):
	pass
	
def remove_user(request,study_id,user_id):
	pass


