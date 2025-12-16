from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        labels = {
            "username": "Логин",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }
        help_texts = {
            "username": "Обязательно. До 150 символов. Только буквы, цифры и @/./+/-/_.",
        }