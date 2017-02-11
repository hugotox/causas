from django.conf import settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from scraper.core.base_page import BasePage


class PopupLocators(object):
    TABS = (By.ID, 'tabs')
    TABLE = (By.CSS_SELECTOR, '.tablaPop')


class Popup(BasePage):
    def __init__(self, driver, profile):
        super().__init__(driver, '')
        self.profile = profile

    def save_to_database(self):
        # TODO: implement this
        pass

    def check_data(self):
        driver = self.driver

        # wait to make sure the new window is loaded
        WebDriverWait(driver, 10).until(lambda d: d.find_element(*PopupLocators.TABS) is not None)

        # there are 2 tables with the same class, first one is the documents table
        table = driver.find_elements(*PopupLocators.TABLE)[0]

        # first row is heading
        heading = True
        rows = table.find_elements_by_tag_name('tr')

        # TODO: save to database
        # TODO: send notification when new document is found
        for row in rows:
            if not heading:
                cols = row.find_elements_by_tag_name('td')
                data = ' - '.join([col.text for col in cols])
                if not self.profile.initial_migration_done:
                    self.save_to_database()

                # send notification only after first migration is done

                print(data)
            heading = False

        if settings.DRIVER == 'chrome':
            driver.close()  # needed when using Chrome
