"""
URL configuration for mainsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db import router
from django.urls import path, include
from django.views.generic import TemplateView


from users_app import api, views, msgr_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authorize/', views.authorize, name = 'authorize'),
    path('registration/', views.registration, name = 'registration'),
    path('api/v0/logout/', views.logout_view, name = 'logout'),


#  Месседжер
    path('', msgr_views.messenger_view, name='index'),
    path('send_message_api/', msgr_views.send_message_api, name='send_message_api'),
    path('check_new_messages_api/', msgr_views.check_new_messages_api, name='check_new_messages'),
    path('get_chats_list_api/', msgr_views.get_chats_list_api, name ='get_chats_list_api'),

    ]
