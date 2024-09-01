from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='user@user.ru',
            first_name='User',
            last_name='User',
            is_staff=True,
            is_active=True,
            is_superuser=False
        )

        user.set_password('user')
        user.save()
