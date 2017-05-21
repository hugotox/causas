from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime
import asyncio
import concurrent.futures

from main.models import UserProfile
from main.scraper import Scraper

logger = get_task_logger(__name__)


def worker(profile):
    print('Scraping for user {}'.format(profile.user.username))
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


@shared_task
def run_scraper():
    users = UserProfile.objects.filter(user__is_active=True)

    async def main():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
            loop = asyncio.get_event_loop()
            futures = []
            for profile in users:
                futures.append(
                    loop.run_in_executor(executor, worker, profile)
                )

            for response in await asyncio.gather(*futures):
                print(response)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
