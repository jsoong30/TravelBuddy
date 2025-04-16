from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Allow letters, digits, underscores, and hyphens in room_slug
    re_path(r'ws/chat/(?P<room_slug>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
]
