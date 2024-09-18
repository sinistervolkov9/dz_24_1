from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random
from lms.models import Course, Lesson

random_code = ''.join(random.sample('0123456789', 6))
NULLABLE = {'blank': True, 'null': True}
PAYMENT_METHODS = [
    ('cash', 'Наличные'),
    ('transfer', 'Перевод на счет'),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


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


# class Payment(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
#     payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', blank=True, null=True)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', blank=True, null=True)
#     # amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
#     amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
#     payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, verbose_name='Способ оплаты', **NULLABLE)
#     session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии')
#     link = models.URLField(max_length=400, blank=True, null=True, verbose_name='Ссылка на оплату')

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payment', on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payment_course', verbose_name='Оплаченный курс', blank=True, null=True)
    stripe_product_id = models.CharField(max_length=255, default='default_product_id')
    stripe_price_id = models.CharField(max_length=255, default='default_value')
    stripe_session_id = models.CharField(max_length=255, default='default_session_id')
    status = models.CharField(max_length=50, default='pending')
    # amount = models.PositiveIntegerField(verbose_name='Сумма оплаты', default=0)

    def __str__(self):
        return f'Платеж от {self.user.email} на сумму {self.course.price}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
