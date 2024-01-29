from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Create 200 users with usernames like user1, user2, etc.'

    def handle(self, *args, **options):
        for i in range(1, 201):
            username = f'user{i}'
            password = username
            User.objects.create_user(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))
