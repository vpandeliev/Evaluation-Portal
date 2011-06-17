from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from portal.studies.views import *
from portal.views import *
#from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	url(r'^$', 'portal.views.home', name="home"),
	(r'^admin/', include(admin.site.urls)),
	(r'^study/',include('portal.studies.urls')),
	url(r'^accounts/login/$',  login, name="login"),
	url(r'^accounts/logout/$', logout, name="logout"),
	url(r'^accounts/register/$', register, name="register"),


	url(r'^video_admin/',  include('portal.video_admin.urls')),


    #(r'^boggle/', include('portal.boggle.urls')),
    
	# Libraries
	(r'^tinymce/', include('tinymce.urls')),
	
)


if settings.DEBUG:
	urlpatterns += patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': settings.MEDIA_ROOT }),
	)

