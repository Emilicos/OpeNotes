from django.db import models

from django.contrib.auth.models import User
from notes.models import Notes

# Create your models here.
class FolderFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    
    @property
    def notes_count(self):
        notes = FolderNotes.objects.filter(folder__id=self.id)
        return len(notes)

    def __str__(self):
        return self.nama


class FolderNotes(models.Model):
    folder = models.ForeignKey(FolderFavorite, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
