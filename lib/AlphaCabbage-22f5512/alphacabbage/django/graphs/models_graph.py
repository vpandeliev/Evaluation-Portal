import imp
from django.conf import settings
from django.db.models.base import ModelBase
from django.utils.importlib import import_module


class ModelsGraph(object):
    
    def __init__(self, g):
        self.g = g
        self.len = 2
        self.models = {}
        self.apps = []
        self.colors = [
            '#6699cc',
            '#66cc99',
            '#9966cc',
            '#99cc66',
            '#cc6699',
            '#cc9966',
            '#99ccff',
            '#99ffcc',
            '#ccff99',
            '#cc99ff',
            '#ff99cc',
            '#ffcc99',            
            ]

    def set_app(self, app):
        self.apps.append(app)

    def color(self):
        return self.colors[len(self.apps)]
    
    def add_model(self, model):
        name = model.__name__
        # Ignore abstracts
        if model._meta.abstract:
            return None
        # Only add once
        if name not in self.models:
            node = self.g.add_node(name, label=name)
            node.style = 'filled'
            node.fillcolor = self.color()
            self.models[name] = node
            for fk in fks_for_model(model):
                self.add_fk(model, fk)
            for m2m in m2ms_for_model(model):
                self.add_m2m(model, m2m)
            for o2o in o2os_for_model(model):
                self.add_o2o(model, o2o)
        else:
            node = self.models[name]
        return node
    
    def add_fk(self, source, fk):
        target = fk.rel.to
        source_node = self.add_model(source)
        target_node = self.add_model(target)
        e = self.g.add_edge(source_node, target_node)
        e.len = self.len
        e.tooltip = '%s.%s ---> %s.%s' % (source.__name__, fk.verbose_name, target.__name__, fk.rel.related_name or '')
        e.color = '#666666'
    
    def add_m2m(self, source, m2m):
        target = m2m.rel.to
        source_node = self.add_model(source)
        target_node = self.add_model(target)
        e = self.g.add_edge(source_node, target_node)
        e.len = self.len
        e.tooltip = '%s.%s <--> %s.%s' % (source.__name__, m2m.verbose_name, target.__name__, m2m.rel.related_name or '')
        e.dir = 'both'
        e.color = '#000000'

    def add_o2o(self, source, o2o):
        target = o2o.rel.to
        source_node = self.add_model(source)
        target_node = self.add_model(target)
        e = self.g.add_edge(source_node, target_node)
        e.len = self.len
        e.tooltip = '%s.%s ---- %s.%s' % (source.__name__, o2o.verbose_name, target.__name__, o2o.rel.related_name or '')
        e.dir = 'none'
        e.color = '#000000'


def make_models_graph(g, ignore_apps=None, **kwargs):
    mg = ModelsGraph(g)
    
    for app in settings.INSTALLED_APPS:
        app_name = app.split('.')[-1]
        if ignore_apps and app_name in ignore_apps:
            continue
        
        mg.set_app(app)
        
        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own admin registration.
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's models.py. For some
        # reason imp.find_module raises ImportError if the app can't be found
        # but doesn't actually try to import the module. So skip this app if
        # its models.py doesn't exist
        try:
            imp.find_module('models', app_path)
        except ImportError:
            continue

        # Step 3: import the app's models file. If this has errors we want them
        # to bubble up.
        module = import_module("%s.models" % app)        
        models = [x for x in module.__dict__.values() if hasattr(x, '__class__') and x.__class__ == ModelBase]
        for model in models:
            mg.add_model(model)


def fks_for_model(model):
    from django.db.models.fields.related import ForeignKey
    for field in model._meta.fields:
        if field.__class__ == ForeignKey:
            yield field

def m2ms_for_model(model):
    for m2m in model._meta.many_to_many:
        yield m2m

def o2os_for_model(model):
    from django.db.models.fields.related import OneToOneField
    for field in model._meta.fields:
        if field.__class__ == OneToOneField:
            yield field
