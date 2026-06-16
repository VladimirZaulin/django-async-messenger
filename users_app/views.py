import time
from datetime import datetime
from dateutil import parser
from http.client import responses
from lib2to3.fixes.fix_input import context

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.messages.context_processors import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from mainsite.settings import DEFAULT_FROM_EMAIL
from .middleware import csrf_check
from users_app.forms import CustomUserCreationForm, LoginForm  # импортирую кастомную базовую модель формы
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout, authenticate
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ChatMessageSerializer
from django.contrib.auth.decorators import login_required
import logging
from functools import wraps



@csrf_check
def authorize(request):
    authform = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if authform.is_valid():
            username = authform.cleaned_data['username']
            password = authform.cleaned_data['password']
            user = authenticate(username=username, password=password)  # Проверяем учетные данные
            if user is not None:
                login(request, user)  # Выполняем вход
                return redirect('/')
    return render(request, 'bootstrap_pages/authorize.html',context={'form':authform})


@api_view(['POST'])
@permission_classes([AllowAny])  # Это уберет ошибку 401 Unauthorized
def logout_view(request):
    if request.user.is_authenticated:
        print("1 # Пытаемся удалить токен только если пользователь распознан")
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass  # Если токена нет (входили через сессию), просто идем дальше
            print(" 2 # Если токена нет (входили через сессию), просто идем дальше")

        logout(request)  # Чистим сессию
        print(" 3 сессия очищена")

    return redirect('/home')  # Или Response({"detail": "success"})



def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Сохраняет пользователя и хеширует пароль
            login(request, user)
            return redirect('/') # Убедитесь, что у вас есть URL с таким именем
    else:
        form = CustomUserCreationForm()
    return render(request, 'bootstrap_pages/registration.html',{'form': form})



