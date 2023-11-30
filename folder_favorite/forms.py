from django import forms

from .models import FolderFavorite

class FolderFavoriteForm(forms.ModelForm):
    class Meta:
        model = FolderFavorite
        fields = ("nama",)