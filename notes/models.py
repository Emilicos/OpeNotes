from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

from course.models import Course
from cloudinary.models import CloudinaryField

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    body = models.TextField(default='')
    created_on = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    photo = CloudinaryField(resource_type="auto",
                            unique_filename=True,
                            folder="openotes/photos", 
                            allowed_formats=["jpg", "jpeg", "png"],
                            blank = True,
                            null = True)
    
    @property
    def score(self):
        votes = Vote.objects.filter(notes__id=self.id)
        return sum(vote.status for vote in votes)
    
    @property
    def children(self):
        return Notes.objects.filter(parent=self).order_by('-created_on').all()
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    # def __str__(self):
    #     return self.title

class Vote(models.Model):
    VOTE_STATUS = (
        (-1, 'Downvote'),
        (1, 'Upvote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
    status = models.IntegerField(choices=VOTE_STATUS)

    def __str__(self):
        return f"{self.user.username} voted {self.get_status_display()} for {self.notes.description}"