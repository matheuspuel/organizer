from django import forms
from .models import Note
from django.contrib.auth.models import User


class NoteForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': 'autofocus',
        'size': '40'
    }))

    class Meta:
        model = Note
        fields = [
            'title',
            'text',
            'category',
            'importance',
        ]
