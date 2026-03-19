from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css_class})
    return field  # Fallback if it's not a form field

@register.filter(name='attr')
def attr(field, attributes):
    from django.forms.boundfield import BoundField
    attrs = {}
    for pair in attributes.split(','):
        if ':' in pair:
            name, value = pair.split(':', 1)
            attrs[name.strip()] = value.strip()
    if isinstance(field, BoundField):
        return field.as_widget(attrs=attrs)
    return field
