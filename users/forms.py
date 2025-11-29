from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User

class UserLoginForm(AuthenticationForm):
    """
    Кастомная форма логина. Наследуем от стандартной,
    чтобы добавить Bootstrap-классы.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Имя пользователя'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Пароль'
        })


class UserRegistrationForm(UserCreationForm):
    """
    Кастомная форма регистрации. Указываем только нужные поля в Meta.
    Django сам создаст поля для username, password1 и password2.
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})


class ProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля. Используем ModelForm.
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})