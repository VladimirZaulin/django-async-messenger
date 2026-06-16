from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=1000,
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Сообщение обязательно',
            'blank': 'Сообщение не может быть пустым',
            'max_length': 'Сообщение слишком длинное'
        }
    )
    # Опциональные поля
    user_id = serializers.IntegerField(required=False)
    conversation_id = serializers.CharField(required=False, max_length=100)

