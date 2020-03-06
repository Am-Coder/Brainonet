from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/groupchat/<room_name>/<token>/', consumers.ChatConsumer),
]