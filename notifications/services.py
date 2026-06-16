from notifications.interfaces import NotificationStrategy
from notifications.models import Notification


class NotificationService:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def send_notification(self, user, title, message) -> bool:
        notification = Notification.objects.create(        
                user=user,
                title=title,
                message=message
        )
        return self.strategy.execute(notification)
    