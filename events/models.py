from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=200)
    joiners = models.ManyToManyField(User, related_name='joined_events', blank=True)

    def __str__(self):
        return self.title
