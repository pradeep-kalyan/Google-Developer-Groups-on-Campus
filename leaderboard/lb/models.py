from django.db import models
from django.contrib.auth.models import User

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)

    def __str__(self):
        return f"Leaderboard Entry: {self.user.user_id} - Points: {self.points}, Streak: {self.streak}"
