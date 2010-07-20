import yapgvb, os.path
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import *
from django.template import Context
from django.template.loader import get_template
from alphacabbage.django.graphs.models import *
from alphacabbage.django.graphs.models_graph import make_models_graph


@staff_member_required
def index(request):
    context = {
        'title': 'Graphs',
    }
    return render_to_response('admin/alphacabbage/graphs/index.html', context)


@staff_member_required
def show_graph(request, graph_type, format):
    context = {
        'title': '%s graph (%s)' % (graph_type.capitalize(), format),
        'link_to_image': reverse('graphs:%s_graph' % graph_type, args=[format]) + '?' + request.META['QUERY_STRING'],
        'format': format,
    }
    return render_to_response('admin/alphacabbage/graphs/show-graph.html', context)


@staff_member_required
def models_graph(request, format):
    g = yapgvb.Digraph('Models')
    # g.rankdir = 'LR'
    engine = request.GET.get('engine', 'dot')
    g.layout(getattr(yapgvb.engines, engine))
    kwargs = {
        'ignore_apps': set('auth admin contenttypes sessions sites graphs'.split(' ')),
    }
    make_models_graph(g, **kwargs)

    # Write to a file in the scratch space
    # we need to do this because writing directly
    # to the response is not yet implemented in yapgvb
    scratch_path = os.path.join(settings.MEDIA_ROOT, 'graphs-scratch', 'models.%s' % (format,))
    g.render(scratch_path)
    scratch = open(scratch_path)

    mimes = {
        'svg': 'image/svg+xml',
        'png': 'image/png',
    }
    # Response
    response = HttpResponse(mimetype=mimes[format])
    response.write(scratch.read())
    return response
