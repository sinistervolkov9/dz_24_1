from django.db import models
from django.contrib.auth.models import AbstractUser
import random

random_code = ''.join(random.sample('0123456789', 6))
NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = models.CharField(max_length=50, default='default_username', verbose_name='Имя пользователя')

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=30, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', default='default user.png', verbose_name="Аватар", **NULLABLE)

    verify_code = models.CharField(max_length=6, default=random_code, verbose_name='Код верификации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        permissions = [
            (
                'set_is_active',
                'Can deactivate user'
            )
        ]
