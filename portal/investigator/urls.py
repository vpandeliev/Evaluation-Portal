from django.conf.urls.defaults import *
from portal.video_conferencing.views import *

urlpatterns = patterns('', 
                       url(r'^$', investigator_home, name='investigator_home'),
                      )
