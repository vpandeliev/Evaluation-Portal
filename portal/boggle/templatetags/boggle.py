from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


register = template.Library()

#<div id="cell-0-0" class="cell col0" letter="{{ board.00 }}">{{ board.00 }}</div>

@register.simple_tag
def boggle_cell(board, row, col):
    letter = board['%s%s' % (row, col)]
    return mark_safe('<div id="cell-%s-%s" class="cell col%s" letter="%s"><div class="container">%s<span class="note"></span></div></div>' % (row, col, col, letter, letter))
