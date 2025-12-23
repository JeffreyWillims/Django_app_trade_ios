from django.shortcuts import redirect
from django.contrib import auth, messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch, Sum, F

from .forms import UserRegistrationForm, ProfileForm, UserLoginForm
from .models import User
from carts.models import Cart
from orders.models import Order, OrderItem


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Представление для входа.
    Переопределяем form_valid для "умного" слияния корзин.
    """
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_message = '%(username)s, вы успешно вошли в аккаунт.'

    def form_valid(self, form):
        session_key = self.request.session.session_key

        # Сначала логиним пользователя
        auth.login(self.request, form.get_user())

        # Теперь, после логина, выполняем слияние
        if session_key:
            try:
                # Находим все анонимные товары
                anonymous_cart_items = Cart.objects.filter(session_key=session_key)
                if anonymous_cart_items.exists():

                    # Проходим по каждому анонимному товару
                    for anon_item in anonymous_cart_items:
                        # Пытаемся найти такой же товар в корзине УЖЕ ЗАЛОГИНЕННОГО пользователя
                        user_item, created = Cart.objects.get_or_create(
                            user=self.request.user,
                            product=anon_item.product
                        )

                        if created:
                            # Если такого товара не было, просто копируем количество
                            user_item.quantity = anon_item.quantity
                        else:
                            # Если был - суммируем
                            user_item.quantity += anon_item.quantity

                        user_item.save()

                    # Удаляем анонимную корзину только после успешного переноса
                    anonymous_cart_items.delete()

            except Exception as e:
                print(f"Ошибка при слиянии корзин: {e}")
                # Не ломаем процесс входа, даже если слияние не удалось

        # Вызываем родительский метод для выполнения редиректа
        return super().form_valid(form)

    def get_success_url(self):
        """
        Возвращает пользователя туда, куда он шел, если есть параметр 'next'.
        """
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('pages:index')


class UserRegistrationView(SuccessMessageMixin, CreateView):
    """
    Представление для регистрации.
    Автоматически логинит пользователя после успешной регистрации.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('pages:index')
    success_message = '%(username)s, вы успешно зарегистрированы и вошли в аккаунт.'

    def form_valid(self, form):
        # Сначала сохраняем пользователя
        response = super().form_valid(form)
        # Затем логиним его
        user = form.instance
        auth.login(self.request, user)
        # И только потом возвращаем редирект
        return response


class UserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление для профиля пользователя с историей заказов.
    """
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'Профиль успешно обновлен.'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'

        orders_queryset = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch("orderitem_set", queryset=OrderItem.objects.select_related("product"))
        ).annotate(
            total_sum=Sum(F('orderitem__quantity') * F('orderitem__price'))
        ).order_by("-created_timestamp")

        paginator = Paginator(orders_queryset, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context


def logout_view(request):
    """
    Функция-представление для выхода пользователя.
    """
    auth.logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect(reverse_lazy('pages:index'))