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
        # 1. Получаем базовый queryset
        queryset = super().get_queryset().select_related('category')

        # --- Начало логики Поиска ---
        query = self.request.GET.get('q')
        if query:
            # Q-объекты позволяют строить сложные запросы с использованием "ИЛИ"
            # Мы ищем совпадение query в поле "name" или в поле 'description'
            # __icontains означает 'содержит, без учета регистра'
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        # --- КОНЕЦ НОВОЙ ЛОГИКИ ПОИСКА ---

        # 2. Получаем 'category_slug' из URL.
        # self.kwargs - это словарь с именованными параметрами из URL.
        # Он заполняется благодаря <slug:category_slug> в твоем urls.py
        category_slug = self.kwargs.get('category_slug')

        # 3. Применяем фильтр по категории, ЕСЛИ мы на странице категории
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # 4. Получаем параметры фильтров и сортировки из GET-запроса
        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by')

        # 5. Применяем фильтр по акции
        if on_sale == 'on':
            queryset = queryset.filter(discount__gt=0)

        # 6. Применяем сортировку
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
    context_object_name = 'product'  # Имя для объекта продукта в шаблоне
    slug_url_kwarg = 'product_slug'  # Явно указываем, какой параметр из URL использовать для поиска

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст заголовок страницы.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context