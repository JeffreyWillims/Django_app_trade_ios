from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        """
        Переопределяем queryset для добавления ВСЕЙ нашей логики:
        1. Фильтрация по категории.
        2. Фильтрация по акции.
        3. Сортировка.
        """
        queryset = super().get_queryset().select_related('category')


        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by')

        if on_sale == 'on':
            queryset = queryset.filter(discount__gt=0)

        if order_by and order_by != 'default':
            queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['categories'] = Category.objects.all()
        context['is_catalog_page'] = True
        return context


class ProductDetailView(DetailView):
    """
    Представление для отображения детальной информации о продукте.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context