from django import forms
from .models import Notes
from cloudinary.models import CloudinaryField

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
    image = forms.ImageField(required=False)
    class Meta:
        model = Notes
        fields = ['body','image']
    