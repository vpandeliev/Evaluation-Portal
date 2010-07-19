from django import template
from django.template.context import Context
from django.template.loader import get_template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from alphacabbage.django.helpers import import_module_from_path


register = template.Library()


@register.filter
def choice(choice_index, path):
    try:
        choices = import_module_from_path(path)
    except ImportError, e:
        return choice_index
    try:
        choice_index = int(choice_index)
    except ValueError:
        return choice_index
    return choices.verbose(choice_index)


@register.simple_tag
def choice_sequence(path, choice_index=None, template_name=None):
    try:
        choices = import_module_from_path(path)
    except ImportError:
        return '<span class="error">Failed to import %s</span>' % path
    try:
        choice_index = int(choice_index)
    except ValueError:
        choice_index = -1
    template_name = template_name or 'choice/sequence.html'
    template = get_template(template_name)
    return template.render(Context({
        'choices': choices,
        'index': choice_index,
        }))
