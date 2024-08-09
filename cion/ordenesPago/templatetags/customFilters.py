# mi_app/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr):
    return getattr(obj, attr, None)
