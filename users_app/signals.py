from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction  # Импортируем транзакции
from .models import Message
from mainsite.celery import app

@receiver(post_save, sender=Message)
def message_created(sender, instance, created, **kwargs):
    if created:
        # Ждем, пока Джанго завершит запись в базу данных
        transaction.on_commit(lambda: send_task_to_queue(instance.id))

def send_task_to_queue(message_id):
    try:
        # Локальный инстанс, который не вешает веб-сокет
        app.send_task(
            'notifications.tasks.send_bg_notifications_task', 
            args=[message_id]
        )
        print(f"Задача отправлена в RabbitMQ для сообщения {message_id}")
    except Exception as e:
        print(f"Ошибка отправки таски: {e}")
