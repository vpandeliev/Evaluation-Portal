from django.conf.urls.defaults import *
from portal.tutorial_study.views import *

urlpatterns = patterns('',
    url(r'^stage_one$', stage_one, name="stage_one"),
    url(r'^stage_two$', stage_two, name="stage_two"),
   
)
