from django.http import *
from django.contrib.auth.decorators import login_required
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.forms import Form, CharField, DateField, ChoiceField, Select


from random import random

class EligibilityForm(Form):
    
    def __init__(self, choices):
        super(EligibilityForm, self).__init__()
        # dynamic fields here ...
        self.fields['study'] = ChoiceField(choices=choices)
    
    # normal fields here ...
    #date_requested = DateField()

#@login_required
def select_study(request):
    # Get the names of all the study folders in the user studies directory
    module_dir = os.path.dirname(__file__) + "/../user_studies"
    files = ["{0}/{1}".format(module_dir, f) for f in os.listdir(module_dir)]
    study_dirs = [f for f in files if os.path.isdir(f)]
    dirs=[os.path.basename(d) for d in study_dirs]
    choices = ( (d, d) for d in dirs )
    
    test_random = random()
    form = EligibilityForm(choices=choices)
    
    return render_to_response('select_study.html', locals(), 
                              context_instance=RequestContext(request))
    