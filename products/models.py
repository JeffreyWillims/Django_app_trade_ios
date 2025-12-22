from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",) # Важно для консистентной пагинации

    def __str__(self):
        return f'Продукт {self.name} | Категория {self.category.name}'

    @property
    def sell_price(self):
        if self.discount:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price