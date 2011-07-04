from django.conf.urls.defaults import *
from portal.study_builder.views import *

urlpatterns = patterns('',
    url(r'^$', build_study, name="build_study"),
)
