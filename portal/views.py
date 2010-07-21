from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def home(request):
	"""docstring for home"""
	return render_to_response("home.html")
	
	
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
	errors = False
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, user)
			# Redirect to a success page.
			return HttpResponseRedirect("/study/")
		else:
			errors = True
			return render_to_response("registration/login.html", locals())
	else:
			return render_to_response("registration/login.html", locals())

def logout(request):
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/")
