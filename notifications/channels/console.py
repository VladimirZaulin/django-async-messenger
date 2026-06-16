import time

from mainsite.settings import DEFAULT_FROM_EMAIL
from notifications.interfaces import NotificationChannel
from notifications.models import Notification

class ConsoleChannel(NotificationChannel):
    def send(self, notification: Notification) -> bool:
        # Логика отправки console
        time.sleep(5)
        x = 3
        for i in range(1, 10000):
            x = 29 * x
        print("Привет, вот и то самое сообщение в консоли")
        return True