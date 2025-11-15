from django.contrib import admin
from .models import Category, Product


# Используем декоратор @admin.register - регистрации моделей, предпочтительнее чем admin.site.register()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Конфигурация для отображения модели Категорий в админ-панели.
    """
    # Автоматически заполняет поле 'slug' на основе поля 'name'.
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Конфигурация для отображения модели Продуктов в админ-панели.
    """
    prepopulated_fields = {'slug': ('name',)}

    # list_display: Какие поля отображать в списке всех продуктов.
    list_display = ('name', 'category', 'price', 'quantity', 'discount')

    # list_editable: Какие поля можно редактировать прямо из списка,
    list_editable = ('price', 'quantity','discount')

    # search_fields: По каким полям будет работать поиск в админке.
    search_fields = ('name', 'description')

    # list_filter: По каким полям можно будет фильтровать продукты в правом сайдбаре.
    list_filter = ('category', 'quantity', 'discount')

    # fields: Определяет порядок и группировку полей на странице редактирования товара.
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "quantity"),
        "discount",     # Поля в одном кортеже будут отображаться на одной строке
    ]