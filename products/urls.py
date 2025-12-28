from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='category'),
    path('product/<slug:product_slug>/', ProductDetailView.as_view(), name='product'),
]