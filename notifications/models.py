from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import OneToOneField, ForeignKey


# Create your models here.
class Notification(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField()
    message = models.TextField()
    NOTIFICATION_TYPES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('TELEGRAM', 'Telegram'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)


class NotificationPreference(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    channels_priority = ArrayField(models.CharField())  # ['EMAIL', 'SMS', 'TELEGRAM']