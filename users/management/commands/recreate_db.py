from django.conf import settings
from django.core.management import BaseCommand
import logging

from users.models import User


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        assert settings.DEBUG
        User.objects.all().delete()
        for x in range(1,6):
            User.objects.create_user(
                username=f'user{x}',
                email=f'user{x}@stam.com',
                first_name=f'first{x}',
                last_name=f'last{x}',
                password='12345'
            )
        User.objects.create_superuser(
            username='eran',
            email='eran@stam.com',
            first_name='eran',
            last_name='eran2',
            password='12345'
        )
        logger.info('Recreate db. There are %d users', User.objects.count())