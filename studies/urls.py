from django.conf.urls.defaults import *
from studies.views import *

urlpatterns = patterns('',

	url(r'^$', show_many_studies, name="show_many_studies"),
	
)
