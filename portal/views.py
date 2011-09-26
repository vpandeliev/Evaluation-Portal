from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
	"""docstring for home"""
	if request.user.is_authenticated():
	    return HttpResponseRedirect("/study/")
	return HttpResponseRedirect("/accounts/login")
	
	
def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/study/")
		else:
			form = UserCreationForm()
			return render_to_response("registration/register.html", {
			'form': form,
			})
	else:
		form = UserCreationForm()
		return render_to_response("registration/register.html", {
		'form': form,
		})

def login(request):
	#if 'next' not in request.REQUEST.keys():
	next = '/study/'
	#else:
	#	next = request.REQUEST['next']
	errors = False
	if request.method == 'POST':

		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, user)
			# Redirect to a success page.
			return HttpResponseRedirect(request.POST.get('next',''))
				
		else:
			errors = True
			return render_to_response("registration/login.html", locals(), context_instance=RequestContext(request))
	else:
			return render_to_response("registration/login.html", locals(), context_instance=RequestContext(request))

def logout(request):
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/")
