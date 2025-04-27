from django.db import models
from django.contrib.auth.models import User
from django.db import models
import datetime
from djangochat.models import Room, RoomMembership
from django.utils.text import slugify


class Review(models.Model):
    itinerary = models.ForeignKey('Itinerary',
                                  on_delete=models.CASCADE,
                                  related_name='reviews')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} / 5") for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('itinerary', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.itinerary.name} review by {self.user.username}"


# --------------------------------------------------

class Itinerary(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    start_date = models.DateField()
    end_date = models.DateField()
    locations = models.JSONField(default=list)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    chat_room = models.OneToOneField(
        'djangochat.Room',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='itinerary'
    )

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        creating = self.pk is None

        super().save(*args, **kwargs)

        if creating and not self.chat_room:
            slug = slugify(f"{self.name}-{self.id}")
            room = Room.objects.create(
                name=f"Chat for {self.name}",
                slug=slug,
                owner=self.user
            )
            # Auto-approve the creator
            RoomMembership.objects.create(
                user=self.user,
                room=room,
                status=RoomMembership.APPROVED
            )
            self.chat_room = room
            super().save(update_fields=['chat_room'])

