"""
NayePankh Foundation - Custom Template Filters
"""

from django import template

register = template.Library()


@register.filter(name='split')
def split_filter(value, delimiter=','):
    """
    Split a string by the given delimiter and return a list.
    Usage: {{ "a, b, c"|split:", " }}  →  ['a', ' b', ' c']
    """
    if not value:
        return []
    return str(value).split(delimiter)


@register.filter(name='trim')
def trim_filter(value):
    """Strip leading/trailing whitespace from a string."""
    if not value:
        return value
    return str(value).strip()
