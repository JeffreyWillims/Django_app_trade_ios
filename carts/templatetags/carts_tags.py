from django import template
from carts.utils import get_user_carts

register = template.Library()

@register.inclusion_tag('carts/includes/included_cart.html', takes_context=True)
def user_cart(context):
    request = context['request']
    carts = get_user_carts(request)
    return {'carts': carts}