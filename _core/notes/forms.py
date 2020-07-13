from django import forms
from .models import Note
from django.contrib.auth.models import User


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = [
            'title',
            'text',
            'category',
            'importance',
        ]

    def __init__(self, request=None, instance=None):
        super().__init__(request, instance=instance)

        self.fields['title'].widget.attrs['style'] = 'width:350px'
