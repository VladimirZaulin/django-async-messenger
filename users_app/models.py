import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

from django.db import models
from django.db.models import CharField


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=32, unique=True, null=True) # в дальнейшем можно добавить валидацию
    birthdate = models.DateField(blank=True, null=True, default=None)
    referred = models.ForeignKey(
     User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='referrals'
)
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)




class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='chat_rooms')
    last_msg_time = models.DateTimeField(auto_now=True) # или auto_now_add=True

    # Здесь могут быть дополнительные поля, например, участники (members)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages') # ДОБАВИЛИ
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

