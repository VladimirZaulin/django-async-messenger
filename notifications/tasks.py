from celery import Celery
import os
from django.apps import apps

# Если Celery запускается отдельно, ему нужно знать, где настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainsite.settings')

if not apps.ready:
    import django
    django.setup()

from users_app.models import Message  # Импорты моделей строго ПОСЛЕ django.setup()
from .channels.telegram import TelegramChannel
from .services import NotificationService
from .strategies import FallbackNotificationStrategy

app = Celery(main="task", broker='amqp://guest:guest@rabbitmq:5672//')

@app.task
def send_bg_notifications_task(message_id):
    try:
        message_instance = Message.objects.get(id=message_id)
        receivers = message_instance.room.members.all()
        
        print(f"--- СТАРТ ТАСКИ ДЛЯ СООБЩЕНИЯ {message_id} ---")
        print(f"Автор сообщения: {message_instance.sender.username}")
        print(f"Всего участников в комнате: {receivers.count()}")
        
        for receiver in receivers:
            print(f"Проверяем участника: {receiver.username}")
            
            if receiver == message_instance.sender:
                print(f"-> Пропускаем {receiver.username}: он автор сообщения")
                continue
                
            if not hasattr(receiver, 'userprofile'):
                print(f"-> Пропускаем {receiver.username}: нет профиля UserProfile")
                continue
                
            chat_id = receiver.userprofile.telegram_chat_id
            print(f"-> У юзера {receiver.username} найден chat_id: {chat_id}")
            
            if not chat_id:
                print(f"-> Пропускаем {receiver.username}: поле telegram_chat_id пустое")
                continue
            
            # Если всё ок, создаем сервисы и шлем
            channel = TelegramChannel()
            strategy = FallbackNotificationStrategy(channels=[channel])
            service = NotificationService(strategy=strategy)
            
            service.send_notification(
                user=receiver, 
                title="Новое сообщение", 
                message=message_instance.text
            )
            print(f"-> КОД ОТПРАВКИ В ТГ ВЫЗВАН ДЛЯ {receiver.username}")
            
    except Exception as e:
        print(f"Ошибка в фоновом таске уведомлений: {e}")
