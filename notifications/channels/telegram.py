from ..interfaces import NotificationChannel
import requests
import os
from dotenv import load_dotenv

class TelegramChannel(NotificationChannel):
    def send(self, notification) -> bool:
        # Если у пользователя нет Telegram Chat ID, то не отправляем уведомление
        if not  notification.user.userprofile.telegram_chat_id:
            return False
        if notification.user.userprofile.telegram_chat_id:
            try:
                TG_TOKEN = os.getenv('TG_TOKEN')
                url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
                payload = {
                    "chat_id": notification.user.userprofile.telegram_chat_id,
                    "text": f"{notification.title}\n\n{notification.message}"
                }
                response = requests.post(url, json=payload, timeout=2.0)
                print(f"Ответ Телеграма: {response.status_code} -> {response.text}")
                return response.status_code == 200
            except requests.RequestException as e:
                print(f"Error sending Telegram notification: {e}")
                return False
