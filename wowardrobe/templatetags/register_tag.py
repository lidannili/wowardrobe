from django import template

register = template.Library()


@register.filter
def replace_str(str):
    return str.replace("&", "-").lower()


@register.filter
def lower(str):
    return str.lower()
