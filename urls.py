from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^study/',include('studies.urls')),
	(r'^accounts/login/$',  login),
	(r'^accounts/logout/$', logout),
	
)

if settings.DEBUG:
	urlpatterns += patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': settings.MEDIA_ROOT }),
	)

