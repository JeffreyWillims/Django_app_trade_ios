import stripe
from django.conf import settings
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .forms import OrderCreateForm
from .models import Order, OrderItem
from carts.models import Cart


stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
class OrderCreateView(CreateView):
    template_name = 'orders/create_order.html'
    form_class = OrderCreateForm

    def dispatch(self, request, *args, **kwargs):
        """
        Переопределяем dispatch, чтобы сначала проверить корзину.
        """
        if not Cart.objects.filter(user=request.user).exists():
            messages.error(request, 'Ваша корзина пуста. Невозможно оформить заказ.')
            return redirect('products:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Создание заказа и сессии оплаты.
        """
        try:
            with transaction.atomic():
                # Создаем заказ
                order = form.save(commit=False)
                order.user = self.request.user
                order.save()

                # Переносим товары из корзины в заказ
                user_carts = Cart.objects.filter(user=self.request.user)
                line_items = []
                for cart_item in user_carts:
                    # Проверка наличия на складе
                    if cart_item.product.quantity < cart_item.quantity:
                        raise ValidationError(f'Недостаточно товара "{cart_item.product.name}" на складе.')

                    OrderItem.objects.create(
                        order=order, product=cart_item.product, name=cart_item.product.name,
                        price=cart_item.product.sell_price, quantity=cart_item.quantity
                    )
                    # Уменьшаем остатки
                    cart_item.product.quantity -= cart_item.quantity
                    cart_item.product.save()

                    # Готовим список товаров для Stripe
                    line_items.append({
                        'price_data': {
                            'currency': 'rub', 'unit_amount': int(cart_item.product.sell_price * 100),
                            'product_data': {'name': cart_item.product.name},
                        },
                        'quantity': cart_item.quantity,
                    })

                # Очищаем корзину и сохраняем ID заказа в сессию
                user_carts.delete()
                self.request.session['last_order_id'] = order.id

            # Создаем сессию оплаты в Stripe
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items, mode='payment',
                success_url='{}{}'.format(settings.YOUR_DOMAIN, reverse('orders:order_success')),
                cancel_url='{}{}'.format(settings.YOUR_DOMAIN, reverse('orders:order_cancel')),
                metadata={'order_id': order.id}
            )
            return redirect(checkout_session.url, code=303)

        except ValidationError as e:
            messages.error(self.request, e.message)
            return self.form_invalid(form)

    def get_initial(self):
        """
        Предзаполняет форму данными пользователя.
        """
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated:
            initial.update({
                'first_name': user.first_name, 'last_name': user.last_name,
                'email': user.email, 'phone_number': user.phone_number
            })
        return initial

    def get_context_data(self, **kwargs):
        """
        Передает в шаблон заголовок и состав корзины.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['carts'] = Cart.objects.filter(user=self.request.user)
        return context


@method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
class OrderSuccessView(TemplateView):
    template_name = 'orders/order_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Заказ успешно оформлен'
        last_order_id = self.request.session.get('last_order_id')
        if last_order_id:
            try:
                context['order'] = Order.objects.get(id=last_order_id)
            except Order.DoesNotExist:
                pass
        return context


class OrderCancelView(TemplateView):
    template_name = 'orders/order_cancel.html'