from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Кастомная модель пользователя. Наследует все поля Django,
    добавляя свои (аватар, телефон).
    """
    image = models.ImageField(
        upload_to='users_images', blank=True, null=True, verbose_name='Аватар'
    )
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Номер телефона'
    )

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username