from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser with the provided username and password'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the superuser')
        parser.add_argument('--password', type=str, help='Password for the superuser')

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = kwargs['username']
        password = kwargs['password']

        if not username or not password:
            self.stdout.write(self.style.ERROR('username, password are required.'))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User "{username}" already exists.'))
            return

        # Create the superuser
        User.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))