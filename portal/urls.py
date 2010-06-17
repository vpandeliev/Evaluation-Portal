from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from views import *
#from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	url(r'^$', home, name="home"),
	(r'^admin/', include(admin.site.urls)),
	(r'^study/',include('studies.urls')),
	url(r'^accounts/login/$',  login, name="login"),
	url(r'^accounts/logout/$', logout, name="logout"),
	url(r'^accounts/register/$', register, name="register"),
	
)

if settings.DEBUG:
	urlpatterns += patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': settings.MEDIA_ROOT }),
	)
