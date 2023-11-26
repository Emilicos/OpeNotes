from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    npm = models.CharField(max_length=10, blank=True, null=True)
    faculty = models.CharField(max_length=128, blank=True)
    study_program = models.CharField(max_length=128, blank=True)
    educational_program = models.CharField(max_length=128, blank=True)