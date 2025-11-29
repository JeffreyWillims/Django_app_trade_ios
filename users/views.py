from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegistrationForm, ProfileForm, UserLoginForm
from .models import User


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Представление для входа. Используем встроенный LoginView.
    Логика слияния корзин вынесена в signals.py.
    """
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_message = '%(username)s, Вы успешно вошли в аккаунт'

    def get_success_url(self):
        # Логика редиректа после входа
        return reverse_lazy('pages:index')


class UserRegistrationView(SuccessMessageMixin, CreateView):
    """
    Представление для регистрации. Используем встроенный CreateView.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('pages:index')
    success_message = '%(username)s, Вы успешно зарегистрированы и вошли в аккаунт'

    # Примечание: после регистрации пользователя нужно автоматически залогинить.
    # Это часто делается в методе form_valid, но для чистоты можно
    # использовать и сигнал user_registered. Пока оставим так.


class UserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление для профиля. Используем UpdateView.
    """
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'Профиль успешно обновлен'

    def get_object(self, queryset=None):
        # UpdateView должен знать, какой объект редактировать. Мы говорим ему: "текущего пользователя".
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        # Логику с заказами пока уберем, чтобы сфокусироваться на аутентификации
        # context['orders'] = Order.objects.filter(user=self.request.user)...
        return context



# =======================================================
# ФУНКЦИЯ ВЫХОДА
# =======================================================
def logout_view(request):
    """
    Функция-представление для выхода пользователя.
    Обрабатывает GET-запрос по ссылке.
    """
    auth.logout(request)
    messages.info(request, f"Вы вышли из аккаунта.")
    return redirect(reverse_lazy('pages:index'))