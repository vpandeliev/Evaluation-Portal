from django.conf.urls.defaults import *
from portal.assess.views import *


urlpatterns = patterns('',
    url(r'^setswitch$', set_switch, name="set_switch"),
    url(r'^done$', ss_done, name="ss_done"),
)
