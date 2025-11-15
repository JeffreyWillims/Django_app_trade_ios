from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = 'products'

urlpatterns = [
    # URL для списка всех продуктов
    path('', ProductListView.as_view(), name='index'),
    # URL для списка продуктов отфильтрованных по категории
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='category'),
    # URL для детальной страницы продукта
    path('product/<slug:product_slug>/', ProductDetailView.as_view(), name='product'),
]