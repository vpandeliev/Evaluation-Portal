from django.conf.urls.defaults import *
from studies.views import *

urlpatterns = patterns('',

	url(r'^$', show_many_studies, name="show_many_studies"),
	url(r'^new$', create_one_study, name="create_one_study"),
	
)
