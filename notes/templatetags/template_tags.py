from django import template
from django.db.models import fields

register = template.Library()


@register.filter
def get_obj_attr(obj, attr):
    return getattr(obj, attr)


@register.filter
def is_date_time(obj):
    return isinstance(obj, fields.DateTimeField)


@register.filter
def is_time(obj):
    return isinstance(obj, fields.TimeField)