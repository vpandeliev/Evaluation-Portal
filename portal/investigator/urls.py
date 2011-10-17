from django.conf.urls.defaults import *
from portal.investigator.views import *

urlpatterns = patterns('', 
                       url(r'^$', investigator_home, name='investigator_home'),
                      )
