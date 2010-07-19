'''Utility functions.

Functions:
    import_module_from_path    
'''


def import_module_from_path(path):
    '''Import a module given a full path.
 
    raises::
        ImportError
    '''
    i = path.rfind('.')
    pkg_name = str(path[:i])
    mod_name = str(path[i+1:])
    pkg = __import__(pkg_name, globals(), locals(), [mod_name])
    return getattr(pkg, mod_name)


def get_pair_or_404(model, relation, id1, id2):
    from django.http import Http404
    from django.db import models
    from django.shortcuts import get_object_or_404
    obj1 = get_object_or_404(model, pk=id1)
    try:
        obj2 = getattr(obj1, relation).get(pk=id2)
    except Exception:
        raise Http404()
    return obj1, obj2
