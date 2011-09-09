from django.http import *
from django.contrib.auth.decorators import login_required
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.forms import Form, CharField, DateField, ChoiceField, Select, BooleanField

#################################################################################
#   DJANGO URLS
#################################################################################




#@login_required
def basic_test(request):    
    test = "basbababa"
    
    return render_to_response('basic_test.html', locals(), 
                              context_instance=RequestContext(request))






