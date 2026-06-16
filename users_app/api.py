from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.messages.context_processors import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from mainsite.settings import DEFAULT_FROM_EMAIL
from users_app.forms import CustomUserCreationForm, LoginForm  # импортирую кастомную базовую модель формы
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, authenticate
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ChatMessageSerializer
from django.contrib.auth.decorators import login_required
import logging


logger = logging.getLogger(__name__)



@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_test_mail_v1(request):
    logger.warning('привет, я зашел по API отправки тест письма')
    # from notifications.channels.email import EmailChannel
    # notifiction = EmailChannel()
    # from notifications.models import Notification
    # empty_note = Notification()
    # notifiction.send(empty_note)
    subject = "Тест"
    message_text = "Приветик, это ебать какое тестовое письмо, ты молодец что прочитал, ещё больший молодец, что отправил."
    recipient_email = "dream9h@gmail.com"
    from django.core.mail import send_mail
    send_mail(
        subject,  # Тема письма
        message_text,  # Текст письма
        DEFAULT_FROM_EMAIL,  # Отправитель (должен быть установлен в settings.py)
        ["dream9h@gmail.com"],  # Получатели (список адресов)
        fail_silently=False  # Если True, ошибки не будут вызывать исключения
    )
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view_v1(request):
    # Удаляем токен пользователя при выходе
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


""" Проверка остатка дней в подписке"""

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_subscription_days(request):
    # serializer = UserSubscriptionSerializer(data = request.data)
    serializer = UserSubscription.objects.get(user=request.user)
    try:
        if serializer:
            end_date = serializer.end_date
            days_left = end_date - datetime.now()
            return Response(days_left = days_left, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)