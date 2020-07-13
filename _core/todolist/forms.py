from django import forms
from . import models
from .widgets import XDSoftDateTimePickerInput, MyDurationWidget


class TaskModelForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y %H:%M', '%d/%m/%Y %H:%M:%S'],
        widget=XDSoftDateTimePickerInput()
    )
    start = forms.DateTimeField(
        required=False,
        input_formats=['%d/%m/%Y %H:%M', '%d/%m/%Y %H:%M:%S'],
        widget=XDSoftDateTimePickerInput()
    )
    duration = forms.DurationField(
        required=False,
        widget=MyDurationWidget(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(size='45', autofocus=True)

    class Meta:
        model = models.Task
        exclude = ['user', 'complete_time', 'deleted']


class TaskQuickModelForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['title']

    title = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': 'autofocus',
        'size': '100%'
    }))
