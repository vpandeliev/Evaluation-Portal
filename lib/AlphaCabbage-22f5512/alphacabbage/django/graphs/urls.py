from django.conf.urls.defaults import *


urlpatterns = patterns('alphacabbage.django.graphs.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<graph_type>models)/as-(?P<format>png|svg)/$', 'show_graph', name='show_graph'),
    url(r'^models_graph.(?P<format>png|svg)$', 'models_graph', name='models_graph'),
)
