from django.conf.urls.defaults import *
from portal.studies.views import *

urlpatterns = patterns('',

	url(r'^$', show_many_studies, name="show_many_studies"),
	url(r'^new$', create_one_study, name="create_one_study"),
	url(r'^show/(\d+)', show_one_study, name="show_one_study"),
	url(r'^edit/(\d+)', edit_one_study, name="edit_one_study"),
	url(r'^remove/(\d+)', remove_one_study, name="remove_one_study"),
	

  
)
