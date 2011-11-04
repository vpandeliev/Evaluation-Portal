from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from portal.users.models import UserRoles


def get_user_redirect(user):
    """Returns the appropriate path for the supplied user to be sent to"""
    user_role = user.get_profile().user_role
    
    if user_role == UserRoles.INVESTIGATOR:
	    return '/investigator/'
    elif user_role == UserRoles.PARTICIPANT:
	    return '/study/'
    else:
	    return '/unknown_user_role/'
    

def home(request):
	"""docstring for home"""
	if request.user.is_authenticated():
	    return HttpResponseRedirect(get_user_redirect(request.user))
	else:    
	    return render_to_response("registration/login.html", locals(), context_instance=RequestContext(request))


def login(request):
	"""Try to log in. Redirects to the appropriate error page if something bad
	happens."""
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		
		if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, user)
			return HttpResponseRedirect(get_user_redirect(user))	
		else:
		    # Bad user 
			return render_to_response("registration/login.html", locals(), context_instance=RequestContext(request))
	else:
	    # Strange request. Send them back to the start
	    return home(request)


def logout(request):
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/")
	
	
	
