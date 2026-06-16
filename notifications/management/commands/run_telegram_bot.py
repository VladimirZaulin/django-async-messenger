from django.core.management.base import BaseCommand
from aiogram.filters import Command, CommandObject
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from asgiref.sync import sync_to_async
from users_app.models import UserProfile

from aiogram import Router
router = Router()

def update_user_telegram(user_id, chat_id):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        user_profile.telegram_chat_id = chat_id
        user_profile.save()
        print(f"Updated Telegram chat ID for user {user_id}")
    except UserProfile.DoesNotExist:
        print(f"UserProfile with user_id {user_id} does not exist")

@router.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    await message.reply("Привет! Я бот для уведомлений от Pohud.Art Я буду отправлять тебе уведомления о новых сообщениях в чатах. Пожалуйста, не отключай уведомления от меня, чтобы не пропустить важные сообщения!")
    if command.args:
        await sync_to_async(update_user_telegram)(user_id=command.args, chat_id=message.chat.id)


class Command(BaseCommand):
    help = 'Run the Telegram bot'

    async def main(self):
        TG_TOKEN = os.getenv('TG_TOKEN')
        bot = Bot(token=TG_TOKEN)
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)
    def handle(self, *args, **kwargs):
        asyncio.run(self.main())

