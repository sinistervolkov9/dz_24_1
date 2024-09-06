from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import random
from lms.models import Course, Lesson

random_code = ''.join(random.sample('0123456789', 6))
NULLABLE = {'blank': True, 'null': True}
PAYMENT_METHODS = [
    ('cash', 'Наличные'),
    ('transfer', 'Перевод на счет'),
]


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


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')

    def __str__(self):
        return f'Платеж от {self.user.email} на сумму {self.amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
