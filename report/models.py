from django.db import models
from notes.models import Notes
from django.contrib.auth.models import User

class Laporan(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    pelapor = models.ForeignKey(User, on_delete=models.CASCADE)
    terlapor = models.ForeignKey(Notes, on_delete=models.CASCADE)
    alasan = models.TextField()
    status = models.BooleanField()

    def __str__(self):
        return f"Laporan {self.id} - {self.pelapor.nama}"