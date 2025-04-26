from django.db import models
from django.contrib.auth.models import User
from django.db import models
import datetime

class Itinerary(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    start_date = models.DateField()
    end_date = models.DateField()
    locations = models.JSONField(default=list)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name
