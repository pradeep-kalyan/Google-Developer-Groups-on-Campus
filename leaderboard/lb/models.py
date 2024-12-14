from django.db import models
from django.contrib.auth.models import User

class Leaderboard(models.Model):
    name = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)

    def __str__(self):
        return self.name
