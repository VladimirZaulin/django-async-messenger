from notifications.interfaces import NotificationStrategy, NotificationChannel
from notifications.models import Notification


class FallbackNotificationStrategy(NotificationStrategy):
    def __init__(self, channels: [NotificationChannel]):
        self.channels = channels

    def execute(self, notification: Notification) -> bool:
        for channel in self.channels:
            if channel.send(notification):
                return True
        return False