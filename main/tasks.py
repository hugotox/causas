from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime

from main.models import UserProfile
from main.scraper import Scraper


logger = get_task_logger(__name__)


@shared_task
def run_scraper():
    users = UserProfile.objects.filter(user__is_active=True)
    for profile in users:
        n1 = datetime.now()
        scraper = Scraper(profile)
        if scraper.login():
            scraper.init_scraping()
            if not profile.initial_migration_done:
                profile.initial_migration_done = True
                profile.save()
        n2 = datetime.now()
        time = n2 - n1
        print('Done in {} minutes.'.format(round(time.seconds / 60, 2)))
