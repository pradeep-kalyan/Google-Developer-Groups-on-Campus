from django.db import models
from django.contrib.auth.models import User  # Import the User model


class Event(models.Model):
    event_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"Event {self.event_id}: {self.name} on {self.date}"