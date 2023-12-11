from django import forms
from .models import Notes
from folder_favorite.models import FolderFavorite

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
    

class AddToFavoritesForm(forms.Form):
    folders = forms.ModelMultipleChoiceField(
        queryset=FolderFavorite.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox mr-2 leading-tight'}),
        label="Pilih folder"
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.is_authenticated:
            self.fields['folders'].queryset = FolderFavorite.objects.filter(user=user)