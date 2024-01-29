import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Send a GET request to 172.18.0.6:8001'

    def handle(self, *args, **options):
        url = "http://172.18.0.6:8001/fetch"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            self.stdout.write(self.style.SUCCESS(f'Successfully sent GET request to {url}'))
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error sending GET request: {e}'))
