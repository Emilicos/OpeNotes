from django import forms
from .models import Notes

class NotesForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'rows': '3',
                'placeholder': 'pusingasujancok'
            }
        )
    )

    class Meta:
        model = Notes
        fields = ['body']
    