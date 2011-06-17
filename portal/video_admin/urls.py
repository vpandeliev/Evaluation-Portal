from django.conf.urls.defaults import *
from portal.video_admin.views import *

urlpatterns = patterns('',
    url(r'^$', list_users_for_video, name="list_users_for_video"),
    url(r'^invite_user?.*$', invite_user, name="invite_user"),
    url(r'^uninvite_user?.*$', uninvite_user, name="uninvite_user"),
    
)
