from celery import shared_task
import logging
from django.core.mail import send_mail
from .models import Course, Subscription

logger = logging.getLogger(__name__)

DEFAULT_FROM_EMAIL = 'sinister.volkov9@yandex.ru'


@shared_task
def send_update_mail_task(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subs_list = Subscription.objects.filter(course=course)

        for sub in subs_list:
            try:
                send_mail(
                    'Курс обновился',
                    f'Курс "{course.title}" обновился!',
                    DEFAULT_FROM_EMAIL,
                    [sub.user.email],
                )
            except Exception as e:
                print(f"Ошибка отправки письма пользователю {sub.user.email}: {e}")
    except Course.DoesNotExist:
        print(f"Курс с id {course_id} не найден")
