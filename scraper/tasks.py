import os

from celery.task import task
from django.conf import settings
from datetime import datetime
from selenium.webdriver import PhantomJS, Chrome

from scraper.causas_page.page import CausasPage
from scraper.main_page.page import MainPage

from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task(name="run_scraper")
def run_scraper():
    n1 = datetime.now()

    if settings.DRIVER == 'chrome':
        driver = Chrome(os.path.join(os.getcwd(), 'drivers', settings.PLATFORM, 'chromedriver'))
    else:
        # default to phantomjs
        driver = PhantomJS(os.path.join(os.getcwd(), 'drivers', settings.PLATFORM, 'phantomjs'))

    driver.set_window_size(1200, 775)

    main_page = MainPage(driver, rut=settings.RUT, clave=settings.CLAVE)
    main_page.open()
    main_page.login()

    causas = CausasPage(driver)
    causas.open()
    causas.init_scraping()  # start the background process

    driver.quit()

    n2 = datetime.now()
    time = n2 - n1

    print('Done in {} minutes.'.format(round(time.seconds / 60, 2)))
