from django.http import *


def require_post(view):
    def wrapped(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseBadRequest('Expected a POST request.')
        return view(request, *args, **kwargs)
    wrapped.__name__ = view.__name__
    return wrapped
