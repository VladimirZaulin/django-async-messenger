import logging

from django.test import TestCase
from notifications.channels.email import EmailChannel
from notifications.models import Notification
from django.contrib.auth.models import User

# Tests are not added to this public repository.