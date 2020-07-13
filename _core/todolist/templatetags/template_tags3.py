from datetime import timedelta, datetime

from django import template
from django.db.models import fields

register = template.Library()


@register.filter
def get_obj_attr(obj, attr):
    return getattr(obj, attr)


@register.filter
def get_type(obj):
    return type(obj)


@register.filter
def format_datetime(value):
    if value is None:
        return ''
    return value.strftime("%d/%m/%Y %H:%M")


@register.filter
def format_timedelta(value, format=None):
    if value is None:
        return ''
    if format == 'dhm':
        remainder = int(value.total_seconds())
        days, remainder = divmod(remainder, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days == 0 and hours == 0 and minutes == 0:
            return ''
        return f'{days}d {hours}:{minutes:02d}'
    else:
        remainder = int(value.total_seconds())
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours == 0 and minutes == 0:
            return ''
        return f'{hours}:{minutes:02d}'

