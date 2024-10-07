import datetime
from .models import User
from celery import shared_task
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def deactivate_user():
    users = User.objects.all()
    current_time = timezone.now()
    print(f'current_time = {current_time}')
    month_ago_day = current_time - datetime.timedelta(days=30)
    print(f'month_ago_day = {month_ago_day}')

    for user in users:
        print(f'user = {user}')
        print(f'{user} last_login = {user.last_login}')
        if user.last_login:
            if user.last_login <= month_ago_day:
                user.is_active = False
                user.save()
                logger.info(f'Юзер {user.id} деактивирован')
