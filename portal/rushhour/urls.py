from django.conf.urls.defaults import *
from portal.rushhour.views import *


urlpatterns = patterns('',
    url(r'^play$', play_rushhour_game, name="rushhour"),
    url(r'^rules$', show_rules, name="rules"),
    url(r'^make$', make_rushhour_game, name="rushhourmaker"),
    url(r'^level$', get_level, name="get_level"),
)
