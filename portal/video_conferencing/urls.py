from django.conf.urls.defaults import *
from portal.video_conferencing.views import *

urlpatterns = patterns('', 
                       url(r'^$', basic_test, name='basic_test')
                      )
