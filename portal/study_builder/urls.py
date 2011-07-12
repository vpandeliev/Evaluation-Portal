from django.conf.urls.defaults import *
from portal.study_builder.views import *

urlpatterns = patterns('', 
                        url(r'^$', select_study, name='select_study'), 
                      )
