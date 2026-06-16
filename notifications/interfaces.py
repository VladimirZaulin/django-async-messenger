from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Notification

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: 'Notification') -> bool:
        pass

class NotificationStrategy(ABC):
    @abstractmethod
    def execute(self, notification: 'Notification') -> bool:
        pass