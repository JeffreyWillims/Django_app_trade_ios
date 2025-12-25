from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from products.models import Product
from .models import Cart
from .utils import get_user_carts


def cart_add(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    user = request.user if request.user.is_authenticated else None
    session_key = request.session.session_key or request.session.create()
    cart_item, created = Cart.objects.get_or_create(
        user=user, session_key=session_key if not user else None, product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        carts = get_user_carts(request)
        cart_component_html = render_to_string('carts/includes/included_cart.html',
                                               {'carts': carts, 'request': request})
        return JsonResponse(
            {'message': f'"{product.name}" добавлен в корзину', 'cart_component_html': cart_component_html,
             'total_quantity': carts.total_quantity() if carts else 0})
    return redirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    # TODO: Проверка прав пользователя
    cart_item.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        carts = get_user_carts(request)
        cart_component_html = render_to_string('carts/includes/included_cart.html',
                                               {'carts': carts, 'request': request})
        return JsonResponse({'message': 'Товар удален', 'cart_component_html': cart_component_html,
                             'total_quantity': carts.total_quantity() if carts else 0})
    return redirect(request.META.get('HTTP_REFERER'))


def cart_change_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            cart_item.quantity -= 1

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        carts = get_user_carts(request)
        cart_component_html = render_to_string('carts/includes/included_cart.html',
                                               {'carts': carts, 'request': request})
        return JsonResponse({'message': 'Количество изменено', 'cart_component_html': cart_component_html,
                             'total_quantity': carts.total_quantity() if carts else 0})
    return redirect(request.META.get('HTTP_REFERER'))