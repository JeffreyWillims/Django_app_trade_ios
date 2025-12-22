from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string

from products.models import Product
from .models import Cart
from .utils import get_user_carts


def cart_add(request, product_slug):
    """
    Добавляет товар в корзину или увеличивает его количество.
    Работает как для авторизованных, так и для анонимных пользователей.
    Возвращает JSON-ответ для AJAX-запросов.
    """
    product = get_object_or_404(Product, slug=product_slug)

    if request.user.is_authenticated:
        # Для авторизованного пользователя
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        # Для анонимного пользователя
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key
        cart_item, created = Cart.objects.get_or_create(session_key=session_key, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    # Если запрос был сделан через AJAX, возвращаем JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        carts = get_user_carts(request)
        cart_component_html = render_to_string(
            'carts/includes/included_cart.html', {'carts': carts, 'request': request}
        )

        response_data = {
            'message': f'Товар "{product.name}" добавлен в корзину.',
            'cart_component_html': cart_component_html,
            'total_quantity': carts.total_quantity() if carts else 0,
        }
        return JsonResponse(response_data)

    # Если это обычный запрос (например, без JavaScript), делаем редирект
    return redirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, cart_id):
    """
    Удаляет товар из корзины.
    Работает как для авторизованных, так и для анонимных пользователей.
    Возвращает JSON-ответ для AJAX-запросов.
    """
    # Мы не можем использовать get_object_or_404 напрямую,
    # так как нужно проверить, что пользователь удаляет свою корзину
    cart_item = Cart.objects.filter(id=cart_id).first()
    if cart_item:
        cart_item.delete()

    # AJAX-ответ (идентичен, но с другим сообщением)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        carts = get_user_carts(request)
        cart_component_html = render_to_string(
            'carts/includes/included_cart.html', {'carts': carts, 'request': request}
        )

        response_data = {
            'message': 'Товар удален из корзини.',
            'cart_component_html': cart_component_html,
            'total_quantity': carts.total_quantity() if carts else 0,
        }
        return JsonResponse(response_data)

    return redirect(request.META.get('HTTP_REFERER'))


def cart_change_quantity(request, cart_id):
    """
    Изменяет количество товара в корзине (увеличить/уменьшить).
    Мы добавим эту логику в будущем.
    """
    # TODO: Реализовать логику для кнопок "+" и "-"
    pass