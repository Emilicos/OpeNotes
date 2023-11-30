from django.db import models
from notes.models import Notes
from django.contrib.auth.models import User

class Laporan(models.Model):
    pelapor = models.ForeignKey(User, on_delete=models.CASCADE)
    terlapor = models.ForeignKey(Notes, on_delete=models.CASCADE)
    alasan = models.TextField()
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Laporan {self.id} - Reviewed: {self.reviewed}"