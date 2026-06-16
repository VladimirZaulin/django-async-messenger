#routing.py
from django.urls import re_path, path
from .consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    # Регулярное выражение для извлечения chat_id из URL-адреса WebSocket
    re_path(r'ws/chat/(?P<chat_id>\d+)/$', ChatConsumer.as_asgi()),
    path('ws/notifications/', NotificationConsumer.as_asgi()),

]
