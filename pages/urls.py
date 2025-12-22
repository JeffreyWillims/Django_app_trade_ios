from django.urls import path
from .views import IndexView, AboutView, DeliveryAndPaymentView

app_name = 'pages'

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('delivery/', DeliveryAndPaymentView.as_view(), name='delivery'),
]