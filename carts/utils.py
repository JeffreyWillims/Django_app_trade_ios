from .models import Cart


def get_user_carts(request):
    """
    Утилита для получения корзины текущего пользователя.
    Работает как для авторизованных, так и для анонимных пользователей.
    """
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product')

    if not request.session.session_key:
        return Cart.objects.none()

    return Cart.objects.filter(session_key=request.session.session_key).select_related('product')