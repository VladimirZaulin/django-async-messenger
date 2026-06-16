import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ChatRoom, Message

@login_required(login_url='/authorize')
def messenger_view(request):
    # Получаем все чаты пользователя
    user_chats = ChatRoom.objects.filter(members=request.user)
    
    print(f"DEBUG: Найдено чатов: {user_chats.count()}")
    
    chats_data = []
    for chat in user_chats:
        partner = chat.members.exclude(id=request.user.id).first()
        
        if not partner:
            continue
            
        last_message = Message.objects.filter(room=chat).order_by('-created_at').first()
        unread_count = Message.objects.filter(
            room=chat, 
            is_read=False
        ).exclude(sender=request.user).count()
        
        initials = partner.username[:2].upper()
        if partner.first_name and partner.last_name:
            initials = f"{partner.first_name[0]}{partner.last_name[0]}".upper()
        
        chat_info = {
            'id': chat.id,
            'partner_name': partner.get_full_name() or partner.username,
            'partner_initials': initials,
            'last_message': last_message.text[:50] if last_message else 'Нет сообщений',
            'last_message_time': last_message.created_at.strftime('%H:%M') if last_message else '',
            'unread_count': unread_count,
            'partner_online': False,
        }
        chats_data.append(chat_info)
        print(f"DEBUG: Чат {chat.id} - {chat_info['partner_name']}")
    
    user_data = {
        'id': request.user.id,
        'username': request.user.username,
    }
    
# Передавай чистые данные (массивы и словари), без json.dumps!
    context = {
    'chats_json': chats_data,  
    'user_json': user_data,
    }
    return render(request, 'bootstrap_pages/messenger/chatWS.html', context)



@login_required
def send_message_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})
    
    try:
        data = json.loads(request.body)
        chat_id = data.get('chat_id')
        text = data.get('text', '').strip()
        
        if not text or not chat_id:
            return JsonResponse({'success': False, 'error': 'Empty message or chat_id'})
        
        chat = ChatRoom.objects.get(id=chat_id, members=request.user)
        message = Message.objects.create(
            sender=request.user,
            room=chat,
            text=text
        )
        
        # Обновляем время последнего сообщения
        chat.last_msg_time = timezone.now()
        chat.save(update_fields=['last_msg_time'])
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'time': timezone.localtime(message.created_at).strftime('%H:%M')
        })
    except ChatRoom.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Chat not found'})
    except Exception as e:
        print(f"ERROR in send_message_api: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def check_new_messages_api(request):
    chat_id = request.GET.get('chat_id')
    
    if not chat_id:
        return JsonResponse({'messages': []})
    
    try:
        chat = ChatRoom.objects.get(id=chat_id, members=request.user)
        messages = Message.objects.filter(room=chat).order_by('created_at')
        
        # Отмечаем как прочитанные
        Message.objects.filter(
            room=chat, 
            is_read=False
        ).exclude(sender=request.user).update(is_read=True)
        
        messages_data = []
        for msg in messages:
            messages_data.append({
                'id': msg.id,
                'text': msg.text,
                'sender_id': msg.sender.id,
                'sender_username': msg.sender.username,
                'time': timezone.localtime(msg.created_at).strftime('%H:%M'),
            })
        print(f"DEBUG API: Найдено сообщений в базе для чата {chat_id}: {len(messages_data)}")
        return JsonResponse({'messages': messages_data})
    except ChatRoom.DoesNotExist:
        return JsonResponse({'messages': []})
    
@login_required
def get_chats_list_api(request):
    user_chats = ChatRoom.objects.filter(members=request.user)
    chats_data = []
    for chat in user_chats:
        partner = chat.members.exclude(id=request.user.id).first()
        if not partner:
            continue
            
        last_message = Message.objects.filter(room=chat).order_by('-created_at').first()
        unread_count = Message.objects.filter(room=chat, is_read=False).exclude(sender=request.user).count()
        
        initials = partner.username[:2].upper()
        if partner.first_name and partner.last_name:
            initials = f"{partner.first_name[0]}{partner.last_name[0]}".upper()
        
        chats_data.append({
            'id': chat.id,
            'partner_name': partner.get_full_name() or partner.username,
            'partner_initials': initials,
            'last_message': last_message.text[:50] if last_message else 'Нет сообщений',
            'last_message_time': last_message.created_at.strftime('%H:%M') if last_message else '',
            'unread_count': unread_count,
            'partner_online': False,
        })
    return JsonResponse({'chats': chats_data})
