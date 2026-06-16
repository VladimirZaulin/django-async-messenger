from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Message


'''Базовая форма v1., без рефералов и промокодов '''
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, required=False)
    last_name = forms.CharField(max_length=45, required=False)
    phone = forms.CharField(max_length=32, required=True)
    birthdate = forms.DateField(required=False)

    class Meta:
        model = User  # ← Используем стандартного User
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'phone', 'birthdate')

    def save(self, commit=True):
        # Сначала сохраняем стандартного User
        user = super().save(commit=commit)
        # 2. Только если данные РЕАЛЬНО записываются в базу (commit=True)
        if commit:
            # Теперь у user точно есть ID, можно работать с профилем
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone')
            profile.birthdate = self.cleaned_data.get('birthdate')
            profile.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    
'''Форма для отправки сообщений в чат'''
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text'] # Выводим только поле текста
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control chat-input',
                'placeholder': 'Введите сообщение...',
                'rows': 3
            })
        }