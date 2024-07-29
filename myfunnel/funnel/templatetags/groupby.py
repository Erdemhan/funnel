from django import template
from itertools import groupby
from operator import itemgetter

register = template.Library()

@register.filter
def groupby_filter(value, arg):
    # Ensure the list is sorted by the same key used for grouping
    sorted_value = sorted(value, key=itemgetter(arg))
    # Use groupby correctly without the 'key' keyword
    grouped_data = groupby(sorted_value, itemgetter(arg))
    return [(key, list(group)) for key, group in grouped_data]
