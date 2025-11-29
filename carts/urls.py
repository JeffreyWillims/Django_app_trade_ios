from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('cart-add/<slug:product_slug>/', views.cart_add, name='cart_add'),
    path('cart-remove/<int:cart_id>/', views.cart_remove, name='cart_remove'),
]