from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def media_url():
    return settings.MEDIA_URL


class ModelLookupNode(template.Node):
    def __init__(self, module_path, model_name, pk_varname, varname):
        self.module_path = module_path
        self.model_name = model_name
        self.pk_var = template.Variable(pk_varname)
        self.varname = varname
    def render(self, context):
        module = __import__(self.module_path, {}, {}, [self.model_name])
        model = getattr(module, self.model_name)
        pk = self.pk_var.resolve(context)
        context[self.varname] = model.objects.get(pk=pk)
        return u''

@register.tag
def model_lookup(parser, token):
    '''
    Usage::
        {% model_lookup path.to.model object_id as varname %}
    '''
    try:
        tag_name, path, pk, _as, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "See doc for %r" % token.contents.split()[0]
    i = path.rfind('.')
    if i == -1:
        raise template.TemplateSyntaxError, "Invalid path to model '%r'" % path
    return ModelLookupNode(path[:i], path[i+1:], pk, varname)