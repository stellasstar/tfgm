from django import template

register = template.Library()

@register.filter(name='get_type')
def get_type(value):
    t = type(value)
    return t.__module__ + "." + t.__name__  