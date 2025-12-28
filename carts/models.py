from django.db import models
from users.models import User
from products.models import Product


class CartQueryset(models.QuerySet):
    """
    Кастомный QuerySet для оптимизации запросов к корзине.
    """
    def total_quantity(self):
        # Вычисляет общее количество товаров в корзине
        if self:
            return sum(cart.quantity for cart in self)
        return 0

    def total_price(self):
        # Вычисляет общую стоимость
        if self:
            return sum(cart.product.sell_price * cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    """
    Модель для элемента корзины. Хранит пользователя/сессию, товар и количество.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')
    session_key = models.CharField(max_length=32, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    objects = CartQueryset.as_manager()

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина для {self.user.username if self.user else "Анонима"} | Товар: {self.product.name}'

    def products_price(self):
        # Стоимость всех единиц этого товара
        return round(self.product.sell_price * self.quantity, 2)