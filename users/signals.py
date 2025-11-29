from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from carts.models import Cart

@receiver(user_logged_in)
def merge_anonymous_cart_with_user_cart(sender, request, user, **kwargs):

    """
    Сигнал, который срабатывает после успешного входа пользователя.
    Объединяет анонимную корзину (по session_key) с корзиной пользователя.
    """
    session_key = request.session.session_key
    if session_key:
        # Удаляем старые корзины пользователя, если они есть
        Cart.objects.filter(user=user).delete()
        # "Передаем" анонимную корзину залогиненному пользователю
        Cart.objects.filter(session_key=session_key).update(user=user)