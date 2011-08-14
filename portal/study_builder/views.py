from django.http import *
from django.contrib.auth.decorators import login_required
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.forms import Form, CharField, DateField, ChoiceField, Select, BooleanField

from random import random

from study_selector import *
from study_builder import *


#################################################################################
#   DJANGO URLS
#################################################################################


#@login_required
def process_select_study_form(request):
    if request.method == 'POST': # If the form has been submitted...
        form = create_study_select_form(request.POST)
        if form.is_valid(): # All validation rules pass
            return render_confirm_build(form.cleaned_data['study'], request)
            
    else:
        form = create_study_select_form(None)
        
    return render_to_response('select_study.html', locals(), 
                              context_instance=RequestContext(request))


#@login_required
def select_study(request):    
    form = create_study_select_form(None)
    
    return render_to_response('select_study.html', locals(), 
                              context_instance=RequestContext(request))


def build_study(request):
    if request.method == 'POST': # If the form has been submitted...
        selected_study = request.POST['study']
    else:
        return HttpResponseRedirect("invalid_request.html")
    
    study_settings = StudySettings(get_study_directory(selected_study))
    add_study_to_db(study_settings)
    
    return render_to_response('build_complete.html', locals(), 
                              context_instance=RequestContext(request))

#################################################################################
#   REDIRECTS
#################################################################################


def render_confirm_build(selected_study, request):
    study_settings = StudySettings(get_study_directory(selected_study))
    study_info = str(study_settings)
    description = str(study_settings.description)
    informed_consent = str(study_settings.informed_consent)
    eligibility = str(study_settings.eligibility)
    reward = str(study_settings.reward)
    instructions = str(study_settings.instructions)
    participants = study_settings.participants
    groups = study_settings.groups
    
    return render_to_response('confirm_build.html', locals(), 
                              context_instance=RequestContext(request))



#################################################################################
#   HELPER FUNCTIONS/CLASSES
#################################################################################


class SelectStudyForm(Form):

  def __init__(self, choices=(), post_request=None):
      if post_request == None:
          super(SelectStudyForm, self).__init__()
      else:
          super(SelectStudyForm, self).__init__(post_request)
          
      # dynamic fields here ...
      self.fields['study'] = ChoiceField(choices=choices)
      
  # normal fields here ...
  test_checkbox = BooleanField(required=False)
  other_test = BooleanField(required=True)
  # So put one boolean field for each


def create_study_select_form(post_request):
    """Scans the folders in the user studies directory and creates a form that
    """
    # Build form choices for all study folders in the user studies directory
    study_directories = get_user_study_names()
    choices = ( (d, d) for d in study_directories )
    
    return SelectStudyForm(choices=choices, post_request=post_request)




  