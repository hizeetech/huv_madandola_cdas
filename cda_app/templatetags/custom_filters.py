from django import template

register = template.Library()

@register.filter
def batch(iterable, size):
    l = len(iterable)
    for ndx in range(0, l, size):
        yield iterable[ndx:min(ndx + size, l)]