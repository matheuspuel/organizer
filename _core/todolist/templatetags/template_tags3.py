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
def pretty(obj):
    if obj is None:
        return ''
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y %H:%M")
    if isinstance(obj, timedelta):
        remainder = int(obj.total_seconds())
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{hours}:{minutes:02d}'
    # if isinstance(obj, timedelta):  # show the number of days too
    #     remainder = int(obj.total_seconds())
    #     days, remainder = divmod(remainder, 86400)
    #     hours, remainder = divmod(remainder, 3600)
    #     minutes, seconds = divmod(remainder, 60)
    #     return f'{days}d {hours}:{minutes:02d}'
    if isinstance(obj, str):
        return obj
    else:
        return obj


@register.filter
def pretty_obj_attr(object, field):
    value = getattr(object, field.name)

    if value is None:
        return ''
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y %H:%M")
    if isinstance(value, timedelta):
        def default():
            remainder = int(value.total_seconds())
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours == 0 and minutes == 0:
                return ''
            return f'{hours}:{minutes:02d}'

        def dhm():
            remainder = int(value.total_seconds())
            days, remainder = divmod(remainder, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            if days ==0 and hours == 0 and minutes == 0:
                return ''
            return f'{days}d {hours}:{minutes:02d}'

        if not hasattr(field, 'pretty_type'):
            return default()
        elif field.pretty_type == 'dhm':
            return dhm()
        else:
            return default()

    if isinstance(value, str):
        return value
    else:
        return value

