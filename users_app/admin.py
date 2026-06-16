from django.contrib import admin
from django.contrib.auth.models import User

# Убираем стандартный UserAdmin, он нам не подходит
from .models import UserProfile, Message, ChatRoom


# Регистрируем кастомную модель User с КОРРЕКТНЫМ классом отображения
@admin.register(UserProfile)
class CustomUserAdmin(admin.ModelAdmin):  
    list_display = ('phone',)
    list_filter = ()
    search_fields = ('username', 'phone')
    readonly_fields = () 


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'text', 'created_at', 'is_read')
    list_filter = ('created_at', 'is_read')
    search_fields = ('sender__username', 'text')

@admin.register(ChatRoom)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_msg_time')
    list_filter = ('last_msg_time',)
    search_fields = ('name', 'members__username')
