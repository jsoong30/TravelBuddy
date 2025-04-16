# chat/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a slug from the room name (e.g., "General Chat" becomes "general-chat")
            self.slug = slugify(self.name)
        super(ChatRoom, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
