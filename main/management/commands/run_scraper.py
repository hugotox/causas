from django.core.management import BaseCommand
from django.conf import settings

from main.tasks import run_scraper


class Command(BaseCommand):
    def handle(self, *args, **options):
        if settings.DEBUG:
            run_scraper()
        else:
            while True:
                run_scraper()
