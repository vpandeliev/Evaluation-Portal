from django import template


register = template.Library()


@register.filter
def latex_arg(arg):
    '''
    Useful to avoid putting a space in front of a latex
    command argument. Because Django will parse the first two
    curly braces in something like "\href{{{ url }}}" and doing
    "\href{ {{ url }}}" messes it up with a leading space.
    
    Example usage::
        \href{{ url|latex_arg }}
    
    Produces::
        \href{http://the.url/}
    '''
    return '{%s}' % arg


@register.filter
def latex_cmd(arg, command_name):
    '''
    Produce a LaTeX command with the given name and argument.
    Do not produce anything if the argument is empty.

    Example usage::
        {{ url|latex_cmd:"href" }}

    Produces::
        \href{http://the.url/}
    '''
    return arg and '\%s{%s}' % (command_name, arg) or ''


@register.simple_tag
def curly(times):
    return '{' * times
