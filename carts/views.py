from django.shortcuts import redirect, get_object_or_404
from products.models import Product
from .models import Cart


def cart_add(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    # Получаем или создаем корзину для текущего пользователя/сессии
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        # Если такой товар уже есть в корзине, увеличиваем количество
        if carts.exists():
            cart = carts.first()
            cart.quantity += 1
            cart.save()
        else:
            # Иначе создаем новый элемент
            Cart.objects.create(user=request.user, product=product, quantity=1)
    else:
        # Логика для анонимного пользователя
        # ... (аналогично, но с session_key) ...
        pass  # Пока пропустим для простоты

    return redirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart.delete()
    return redirect(request.META.get('HTTP_REFERER'))