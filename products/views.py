from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category


class ProductListView(ListView):
    """
    Представление для отображения списка всех продуктов,
    с возможностью фильтрации по категориям.
    """
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'  # Имя, под которым список продуктов будет доступен в шаблоне
    paginate_by = 9  # Включаем пагинацию для масштабируемости

    def get_queryset(self):
        """
        Переопределяем queryset для добавления фильтрации и оптимизации.
        """
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')

        # Оптимизация: select_related загружает данные категории одним JOIN-запросом,
        # предотвращая "N+1" проблему. Это критически важно для производительности.
        if category_slug:
            return queryset.filter(category__slug=category_slug).select_related('category')

        return queryset.select_related('category')

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст список всех категорий для отображения в сайдбаре.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """
    Представление для отображения детальной информации о продукте.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'  # Имя для объекта продукта в шаблоне
    slug_url_kwarg = 'product_slug'  # Явно указываем, какой параметр из URL использовать для поиска

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context