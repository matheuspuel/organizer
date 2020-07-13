from django.forms import DateTimeInput, MultiWidget, NumberInput
from django import forms
import datetime


class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/xdsoft_datetimepicker.html'


class MyDurationWidget(forms.TextInput):
    template_name = 'widgets/my_duration_widget.html'
    supports_microseconds = False

    def format_value(self, value):
        if value:
            days_time = value.split(' ')
            if len(days_time) == 2:
                days, time = days_time
            else:
                days = 0
                time, = days_time
            hours, minutes, seconds = time.split(':')
            value = datetime.timedelta(days=int(days), hours=int(hours), minutes=int(minutes))

            remainder = int(value.total_seconds())
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)

            return f'{hours}:{minutes:02}'
        return None

    def value_from_datadict(self, data, files, name):
        duration = super().value_from_datadict(data, files, name)
        if duration == '':
            return None
        hours_minutes = duration.split(':')
        if len(hours_minutes) == 2:
            hours, minutes = hours_minutes
        else:
            hours = 0
            minutes, = hours_minutes
        if hours == '':
            hours = 0
        if minutes == '':
            minutes = 0
        return f'{hours}:{minutes}:00'

