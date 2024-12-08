from django.db import models

# Create your models here.
# events/models.py
from django.db import models

class Event(models.Model):
    event_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"Event {self.event_id}: {self.name} on {self.date}"
