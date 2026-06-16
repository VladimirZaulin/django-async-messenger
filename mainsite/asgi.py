import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainsite.settings')

# Инициализируем стандартное HTTP Django ASGI приложение заранее
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import users_app.routing

application = ProtocolTypeRouter({
    # 1. Если протокол http — отдаем управление стандартным вьюхам и urls.py
    "http": django_asgi_app,
    
    # 2. Если протокол websocket — пропускаем через авторизацию кук/сессий Django 
    # и отдаем нашему routing.py, который свяжет сокет с ChatConsumer
    "websocket": AuthMiddlewareStack(
        URLRouter(
            users_app.routing.websocket_urlpatterns
        )
    ),
})
