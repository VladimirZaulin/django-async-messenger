from mainsite.settings import DEFAULT_FROM_EMAIL
from notifications.interfaces import NotificationChannel
from notifications.models import Notification
from django.core.mail import send_mail

class EmailChannel(NotificationChannel):
    def send(self, notification: Notification) -> bool:
        # Логика отправки email
        # subject = notification.title
        subject = "Тест"
        # message_text = notification.message
        message_text = "Приветик, это ебать какое тестовое письмо, ты молодец что прочитал, ещё больший молодец, что отправил."
        recipient_email = "dream9h@gmail.com"
        send_mail(
            subject,  # Тема письма
            message_text,  # Текст письма
            DEFAULT_FROM_EMAIL,  # Отправитель (должен быть установлен в settings.py)
            [recipient_email],  # Получатели (список адресов)
            fail_silently=False  # Если True, ошибки не будут вызывать исключения
        )
        # print(f"Sending email to {notification.user.email}: {notification.title}")
        return True