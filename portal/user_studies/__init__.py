# we can put anything we want here. This can read all the directories in here
# and do some setup???

# This file must create the urls.py and views.py appropriately for each study.
#   For a given study we need:
#       urls.py:
#           one 
#
import os, sys


urls_file_template = r"""
from django.conf.urls.defaults import *
from portal.tutorial_study.views import *

urlpatterns = patterns('', {0})
"""

stage_url_template = "url(r'^{0}$', {0}, name='{0}')"



#url(r'^stage_two$', stage_two, name="stage_two"),


# how about this:
study_dirs = [f for f in os.listdir() if os.path.isdir(f)]

url_args = [("") for s in generated_studies]
patterns_args = map(url, *x for x in url_args)
urlpatterns = patterns(*patterns_args)
