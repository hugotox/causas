from django.conf import settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper.causas_page.locators import CausasPageLocators
from scraper.causas_page.popup import Popup
from scraper.core.base_page import BasePage


class CausasPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, 'https://oficinajudicialvirtual.pjud.cl/busqueda_por_rut.php')
        self.main_window = None

    def is_archived(self, form, locator):
        """
        Locator is the `form` object found in locators.FORMS_XPATH
        E.g. (By.XPATH, "//form[@action='./causas/causa_suprema2.php']")
        """
        status_list = ['concluida', 'concluída', 'concluidas', 'concluídas', 'archivada', 'archivadas']

        try:
            tr = form.find_element_by_xpath('parent::td/parent::tr')
            # based on the locator I know which tab I'm working on the locator
            if locator[1] == CausasPageLocators.FORM_SUPREMA:
                tab_idx = 4
            elif locator[1] == CausasPageLocators.FORM_APELACIONES:
                tab_idx = 5
            elif locator[1] == CausasPageLocators.FORM_CIVIL:
                tab_idx = 5
            elif locator[1] == CausasPageLocators.FORM_LABORAL:
                tab_idx = 5
            elif locator[1] == CausasPageLocators.FORM_PENAL:
                tab_idx = 6
            elif locator[1] == CausasPageLocators.FORM_COBRANZA:
                tab_idx = 0  # TODO save this on a DB because there is no `Estado causa` column
            elif locator[1] == CausasPageLocators.FORM_FAMILIA:
                tab_idx = 5
            else:
                return False
            estado = tr.find_elements_by_tag_name('td')[tab_idx]
            return estado.text.lower() in status_list
        except:
            pass

        return False

    def loop_forms(self, forms, locator):
        driver = self.driver
        for form in forms:
            if not self.is_archived(form, locator):
                print('Submitting form {}...'.format(locator[1]))
                form.submit()
                # wait to make sure there are two windows open
                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)

                # switch windows
                driver.switch_to.window('popup')

                popup = Popup(self.driver)
                popup.check_data()
                driver.switch_to.window(self.main_window)

    def init_scraping(self):
        driver = self.driver
        self.main_window = driver.current_window_handle

        # tab content is loaded using ajax so we need to wait for it...
        for locator in CausasPageLocators.FORMS_XPATHS:
            WebDriverWait(driver, settings.WEB_DRIVER_WAIT_TIMEOUT).until(
                EC.presence_of_element_located(locator['form'])  # takes a tuple as argument so no need for *
            )

            # click on the tab
            driver.find_element(*locator['tab']).click()

            next_link = True
            while next_link:
                try:
                    forms = driver.find_elements(*locator['form'])
                    self.loop_forms(forms, locator['form'])
                except:
                    pass

                try:
                    next_link = driver.find_element(*locator['next_link'])
                    next_link.click()
                    WebDriverWait(driver, settings.WEB_DRIVER_WAIT_TIMEOUT).until(
                        EC.presence_of_element_located(locator['form'])  # takes a tuple as argument so no need for *
                    )
                except:
                    next_link = None
