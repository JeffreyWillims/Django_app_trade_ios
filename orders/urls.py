from django.urls import path
from .views import OrderCreateView, OrderSuccessView, OrderCancelView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create_order'),
    path('order-success/', OrderSuccessView.as_view(), name='order_success'),
    path('order-cancel/', OrderCancelView.as_view(), name='order_cancel'),
]