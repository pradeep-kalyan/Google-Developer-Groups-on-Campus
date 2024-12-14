from django.db import models
from django.contrib.auth.models import User
# from .models import Event

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# class Participant(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='members')
#     event = models.ManyToManyField(Event, related_name='participants')
#     # score = models.IntegerField()

#     def __str__(self):
#         return f"{self.user.username} at {self.event.name} with score {self.score}"

