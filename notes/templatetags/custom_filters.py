# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='highlight')
def highlight(value, search_query):
    if search_query:
        highlighted_value = value.replace(search_query, f"<span class='highlight'>{search_query}</span>")
        return highlighted_value
    return value
