import datetime
from .models import User
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def deactivate_user():
    users = User.objects.all()
    current_time = datetime.datetime.now()
    month_ago_day = current_time - datetime.timedelta(days=30)

    for user in users:
        if user.last_login <= month_ago_day:
            user.is_active = False
            user.save()
            logger.info(f'Юзер {user.id} деактивирован')
