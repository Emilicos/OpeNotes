from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    credit = models.IntegerField(default = 0)
    description = models.TextField(default = "")
    semester = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.name