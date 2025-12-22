from django.db import models
from users.models import User

class Order(models.Model):
    # Статусы заказа
    CREATED = 'CREATED'
    PAID = 'PAID'
    ON_WAY = 'ON_WAY'
    DELIVERED = 'DELIVERED'
    STATUSES = [
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    ]

    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True,
                             verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(max_length=254, verbose_name='Email')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=250, verbose_name='Адрес доставки')

    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    status = models.CharField(max_length=50, choices=STATUSES, default=CREATED, verbose_name='Статус заказа')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_timestamp',)

    def __str__(self):
        return f"Заказ №{self.id} | {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(to='products.Product', on_delete=models.SET_DEFAULT, default=None, null=True,
                                verbose_name='Продукт')
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'

    def __str__(self):
        return f"Товар '{self.name}' для заказа №{self.order.id}"