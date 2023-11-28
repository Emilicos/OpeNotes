from django.contrib.auth.models import User
from django.db import models

from course.models import Course

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="")
    description = models.TextField(default="")

    def __str__(self):
        return self.title
