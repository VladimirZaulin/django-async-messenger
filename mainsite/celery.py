import os
from celery import Celery

# Устанавливаем дефолтные настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainsite.settings')

# Создаем инстанс Celery. Слово 'mainsite' должно совпадать с именем папки проекта
app = Celery('mainsite')

# Читаем настройки из settings.py с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем таски во всех установленных приложениях (в т.ч. в notifications)
app.autodiscover_tasks()
