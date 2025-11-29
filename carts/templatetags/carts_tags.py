from django import template
from carts.models import Cart

register = template.Library()


@register.inclusion_tag('carts/includes/cart_counter.html', takes_context=True)
def cart_counter(context):
    """
    Тег для рендеринга счетчика товаров в корзине (в шапке сайта).
    """
    request = context['request']
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        carts = Cart.objects.filter(session_key=request.session.session_key)

    return {'carts': carts}


@register.inclusion_tag('carts/includes/included_cart.html', takes_context=True)
def user_cart_component(context):
    """
    Тег для рендеринга КОМПОНЕНТА КОРЗИНЫ ЦЕЛИКОМ.
    Он сам получает данные и передает их в свой шаблон.
    """
    request = context['request']
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user).select_related('product')
    else:
        if not request.session.session_key:
            request.session.create()
        carts = Cart.objects.filter(session_key=request.session.session_key).select_related('product')

    return {'carts': carts}