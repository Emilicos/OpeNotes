from django.db import models

from django.contrib.auth.models import User
from notes.models import Notes

# Create your models here.
class FolderFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    
    def notes_count(self):
        return self.folder_notes.count()
    
    def __str__(self):
        return self.nama


class FolderNotes(models.Model):
    folder = models.ForeignKey(FolderFavorite, on_delete=models.CASCADE, related_name='folder_notes')
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
