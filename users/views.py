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
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_message = '%(username)s, вы успешно вошли в аккаунт.'

    def form_valid(self, form):
        # 1. ЗАПОМИНАЕМ СТАРЫЙ КЛЮЧ
        session_key = self.request.session.session_key
        # 2. ЛОГИНИМ ПОЛЬЗОВАТЕЛЯ (СЕССИЯ МЕНЯЕТСЯ)
        user = form.get_user()
        auth.login(self.request, user)
        # 3. ВЫПОЛНЯЕМ СЛИЯНИЕ ПО СТАРОМУ КЛЮЧУ
        if session_key:
            try:
                anon_cart = Cart.objects.filter(session_key=session_key)
                if anon_cart.exists():
                    for item in anon_cart:
                        cart_item, created = Cart.objects.get_or_create(user=user, product=item.product)
                        cart_item.quantity += item.quantity
                        cart_item.save()
                    anon_cart.delete()
            except Exception as e:
                print(f"Login cart merge error: {e}")
        # 4. ДЕЛАЕМ РЕДИРЕКТ
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url or reverse_lazy('pages:index')


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('pages:index')
    success_message = '%(username)s, вы успешно зарегистрированы.'

    def form_valid(self, form):
        # 1. ЗАПОМИНАЕМ СТАРЫЙ КЛЮЧ
        session_key = self.request.session.session_key
        # 2. СОХРАНЯЕМ И ЛОГИНИМ ПОЛЬЗОВАТЕЛЯ
        user = form.save()
        auth.login(self.request, user)
        # 3. ВЫПОЛНЯЕМ СЛИЯНИЕ ПО СТАРОМУ КЛЮЧУ
        if session_key:
            try:
                anon_cart = Cart.objects.filter(session_key=session_key)
                if anon_cart.exists():
                    for item in anon_cart:
                        cart_item, created = Cart.objects.get_or_create(user=user, product=item.product)
                        cart_item.quantity += item.quantity
                        cart_item.save()
                    anon_cart.delete()
            except Exception as e:
                print(f"Registration cart merge error: {e}")
        # 4. ДЕЛАЕМ РЕДИРЕКТ
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.success_url)

# ... UserProfileView и logout_view остаются БЕЗ ИЗМЕНЕНИЙ ...
class UserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'Профиль успешно обновлен.'
    def get_object(self, queryset=None): return self.request.user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        orders_queryset = Order.objects.filter(user=self.request.user).prefetch_related(Prefetch("orderitem_set", queryset=OrderItem.objects.select_related("product"))).annotate(total_sum=Sum(F('orderitem__quantity') * F('orderitem__price'))).order_by("-created_timestamp")
        paginator = Paginator(orders_queryset, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
def logout_view(request):
    auth.logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect(reverse_lazy('pages:index'))