from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    preview = models.ImageField(verbose_name='Картинка', upload_to='course_previews/', **NULLABLE)
    description = models.TextField(verbose_name='Описание',)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, related_name='courses',
                             verbose_name='Пользователь')
    lesson = models.ManyToManyField('Lesson', verbose_name='Уроки', related_name='course_lessons')

    price = models.PositiveIntegerField(verbose_name='Стоимость курса', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание',)
    preview = models.ImageField(verbose_name='Картинка', upload_to='lesson_previews/', **NULLABLE)
    video_url = models.URLField(verbose_name='Ссылка на видео', max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, related_name='lessons',
                             verbose_name='Пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Пользователь')
    course = models.ForeignKey('lms.Course', on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Курс')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} подписан на {self.course}'
