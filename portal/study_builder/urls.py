from django.conf.urls.defaults import *
from portal.study_builder.views import *

urlpatterns = patterns('', 
                       url(r'^$', select_study, name='select_study'),
                       url(r'^process_select_study_form$', process_select_study_form, name='select_study'),
                       url(r'^build_study$', build_study, name='build_study'),
                        
                      )
