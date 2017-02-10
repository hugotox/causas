from django.http import HttpResponse
from scraper.tasks import run_scraper


def home(request):
    # run_scraper.delay()
    return HttpResponse('ok')

