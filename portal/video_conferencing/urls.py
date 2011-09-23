from django.conf.urls.defaults import *
from portal.video_conferencing.views import *

urlpatterns = patterns('', 
                       url(r'^$', basic_test, name='basic_test'),
                       url(r'^invite_user.*$', invite_user, name='invite_user'),
                       url(r'^uninvite_user.*$', uninvite_user, name='uninvite_user')
                       
                      )
