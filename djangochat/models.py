from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_rooms'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='RoomMembership',
        related_name='chat_rooms'
    )
    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages',
                             on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

class RoomMembership(models.Model):
    PENDING  = 0
    APPROVED = 1
    DENIED   = 2
    STATUS_CHOICES = [
        (PENDING,  'Pending'),
        (APPROVED, 'Approved'),
        (DENIED,   'Denied'),
    ]

    user         = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE)
    room         = models.ForeignKey(Room, on_delete=models.CASCADE)
    status       = models.PositiveSmallIntegerField(
                       choices=STATUS_CHOICES,
                       default=PENDING
                   )
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','room')
