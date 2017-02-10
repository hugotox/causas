from django.core.management import BaseCommand

from scraper.tasks import run_scraper


class Command(BaseCommand):
    def handle(self, *args, **options):
        run_scraper()
