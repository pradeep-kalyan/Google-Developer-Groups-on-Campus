from django.db import models
from django.contrib.auth.models import User

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

    
# users/models.py

# class User(models.Model):
#     user_id = models.IntegerField(unique=True)
#     points = models.IntegerField(default=0)
#     streak = models.IntegerField(default=0)
#     last_attended_event = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return f"User {self.user_id}: Points={self.points}, Streak={self.streak}"
