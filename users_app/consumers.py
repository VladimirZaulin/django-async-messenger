#consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, Message

#TODO №1: Редактирование сообщений (Message Editing)
# Что сделать на бэкенде (consumers.py):
# В receive: Добавить проверку поля action в JSON. Если action == 'edit', вызывать метод изменения.
# В БД (@database_sync_to_async): Создать метод edit_message(msg_id, new_text). Добавить в него проверку: Message.objects.get(id=msg_id).sender == self.user (чтобы чужие сообщения никто не правил).
# В group_send: Отправить в группу событие с типом type: 'message_edited', передав id сообщения и new_text.
# В классе: Написать метод-обработчик async def message_edited(self, event), который пересылает этот JSON на фронтенд.
# ⚠️ Не забыть на фронтенде:
# Добавить кнопку «Редактировать» у своих сообщений, которая превращает текст в поле ввода.
# При отправке измененного текста слать в вебсокет JSON вида: {"action": "edit", "id": 123, "text": "новый текст"}.
# В коде приема сообщений (onmessage) от вебсокета обработать тип message_edited: найти на странице элемент сообщения с нужным id и заменить в нем текст.
#TODO №2: Плашка с датой для первого сообщения за день (Date Separator)
# Что сделать на бэкенде (consumers.py):
# В БД (save_message): Перед созданием сообщения сделать запрос в базу: есть ли сообщения в этой комнате за сегодня (created_at__date=timezone.now().date()).
# В ответе: Если сообщений не было, добавить в возвращаемый словарь флаг 'show_date_separator': True и саму дату строкой (например, «26 мая»). Если сообщения были — передавать False.
# В group_send: Этот флаг автоматически улетит всем участникам через текущую логику рассылки.
# ⚠️ Не забыть на фронтенде:
# В коде приема сообщений (onmessage) проверять поле show_date_separator.
# Если оно true, то перед тем, как отрендерить само сообщение, вставить в чат красивый HTML-блок во всю ширину с текстом даты (например, <div class="date-separator">26 мая</div>).

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.user = self.scope["user"]

        # Проверяем, авторизован ли пользователь
        if not self.user.is_authenticated:
            await self.close()
            return

        # Проверяем доступ к комнате
        if not await self.check_room_access():
            await self.close()
            return

        # Присоединяемся к группе чата
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу чата при отключении
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Получение сообщения от фронтенда (браузера)
    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('text', '').strip()

        if not text:
            return

        # Сохраняем сообщение в БД и обновляем комнату
        msg_data = await self.save_message(text)

        # Отправляем сообщение всем участникам группы чата
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': msg_data['id'],
                'text': msg_data['text'],
                'sender_id': self.user.id,
                'sender_username': self.user.username,
                'time': msg_data['time']
            }
        )
        await self.notify_chat_members(msg_data)

    # Метод-обработчик события 'chat_message' для рассылки в браузеры
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'text': event['text'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'time': event['time']
        }))

    async def notify_chat_members(self, msg_data):
        try:
            # Получаем список ID участников комнаты (кроме текущего пользователя)
            # Для этого напишем маленький синхронный хелпер чуть позже
            receiver_ids = await self.get_room_receiver_ids()
            
            for receiver_id in receiver_ids:
                await self.channel_layer.group_send(
                    f'user_{receiver_id}',
                    {
                        'type': 'chat_list_update',  # Имя метода-обработчика
                        'chat_id': self.chat_id,
                        'text': msg_data['text'],
                        'time': msg_data['time'],
                        'sender_id': self.user.id,
                    }
                )
        except Exception as e:
            print(f"Ошибка при отправке уведомления в список чатов: {e}")

    # --- Синхронные методы работы с БД, обернутые для асинхронной среды ---
    @database_sync_to_async
    def check_room_access(self):
        return ChatRoom.objects.filter(id=self.chat_id, members=self.user).exists()

    @database_sync_to_async
    def save_message(self, text):
        room = ChatRoom.objects.get(id=self.chat_id)
        msg = Message.objects.create(sender=self.user, room=room, text=text)
        
        # Обновляем время последнего сообщения в комнате
        room.last_msg_time = timezone.now()
        room.save(update_fields=['last_msg_time'])
        
        return {
            'id': msg.id,
            'text': msg.text,
            'time': timezone.localtime(msg.created_at).strftime("%H:%M")
        }
    
    @database_sync_to_async
    def get_room_receiver_ids(self):
        room = ChatRoom.objects.get(id=self.chat_id)
        # Забираем ID всех участников, кроме текущего пользователя
        return list(room.members.exclude(id=self.user.id).values_list('id', flat=True))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.user_group_name = f'user_{self.user.id}'
        
        # Подключаем пользователя к его персональной группе
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    # Прилетает триггер от Celery или сокета другого юзера
    async def chat_list_update(self, event):
        # Шлем на фронт чистую команду-триггер без лишней воды
        await self.send(text_data=json.dumps({
            'type': 'chat_list_update'
        }))
