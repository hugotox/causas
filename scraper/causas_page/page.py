from django.conf import settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from main.models import Causa
from scraper.causas_page.locators import CausasPageLocators
from scraper.causas_page.popup import Popup
from scraper.core.base_page import BasePage


class CausasPage(BasePage):
    def __init__(self, driver, profile):
        super().__init__(driver, 'https://oficinajudicialvirtual.pjud.cl/busqueda_por_rut.php')
        self.profile = profile
        self.main_window = None

    def get_tipo_causa(self, locator):
        """
        Locator is the `form` object found in locators.FORMS_XPATH
        E.g. (By.XPATH, "//form[@action='./causas/causa_suprema2.php']")
        """
        if locator[1] == CausasPageLocators.FORM_SUPREMA:
            type = Causa.TYPE_CHOICES_SUPREMA
        elif locator[1] == CausasPageLocators.FORM_APELACIONES:
            type = Causa.TYPE_CHOICES_APELACIONES
        elif locator[1] == CausasPageLocators.FORM_CIVIL:
            type = Causa.TYPE_CHOICES_CIVIL
        elif locator[1] == CausasPageLocators.FORM_LABORAL:
            type = Causa.TYPE_CHOICES_LABORAL
        elif locator[1] == CausasPageLocators.FORM_PENAL:
            type = Causa.TYPE_CHOICES_PENAL
        elif locator[1] == CausasPageLocators.FORM_COBRANZA:
            type = Causa.TYPE_CHOICES_COBRANZA
        elif locator[1] == CausasPageLocators.FORM_FAMILIA:
            type = Causa.TYPE_CHOICES_FAMILIA
        else:
            return None
        return type

    def get_or_create_form_to_cause(self, form, tipo_causa):

        tr = form.find_element_by_xpath('parent::td/parent::tr')

        # based on the locator I know which tab I'm working on the locator
        if tipo_causa == Causa.TYPE_CHOICES_SUPREMA:
            idx_cara = 2
            idx_status = 4
        elif tipo_causa == Causa.TYPE_CHOICES_APELACIONES:
            idx_cara = 3
            idx_status = 5
        elif tipo_causa == Causa.TYPE_CHOICES_CIVIL:
            idx_cara = 3
            idx_status = 5
        elif tipo_causa == Causa.TYPE_CHOICES_LABORAL:
            idx_cara = 3
            idx_status = 5
        elif tipo_causa == Causa.TYPE_CHOICES_PENAL:
            idx_cara = 4
            idx_status = 6
        elif tipo_causa == Causa.TYPE_CHOICES_COBRANZA:
            idx_cara = 3
            idx_status = 0  # TODO identify when a cobranza is archived
        elif tipo_causa == Causa.TYPE_CHOICES_FAMILIA:
            idx_cara = 3
            idx_status = 5
        else:
            return None

        archived_status_list = ['concluida', 'concluída', 'concluidas', 'concluídas', 'archivada', 'archivadas', 'arc',
                                'arc.', 'arch', 'arch.']

        form_id = '{}_{}'.format(tipo_causa, tr.find_elements_by_tag_name('td')[1].text.lower().replace('&nbsp;', '').strip())
        caratulado = tr.find_elements_by_tag_name('td')[idx_cara].text
        estado = tr.find_elements_by_tag_name('td')[idx_status].text.lower()

        try:
            causa = Causa.objects.get(id=form_id)
        except Exception as ex:
            causa = Causa(id=form_id, user=self.profile, type=tipo_causa, archived=False, caratulado=caratulado)
            causa.save()

        return causa

    def loop_forms(self, forms, locator):
        driver = self.driver
        for form in forms:

            # saves the form to the database if it wasn't saved before
            tipo_causa = self.get_tipo_causa(locator)
            causa = self.get_or_create_form_to_cause(form, tipo_causa)

            if causa and not causa.archived:
                print('Submitting form {}...'.format(tipo_causa))

                # form submit opens the cause details in a popup window
                form.submit()
                # wait to make sure there are two windows open
                WebDriverWait(driver, settings.WEB_DRIVER_WAIT_TIMEOUT).until(lambda d: len(d.window_handles) == 2)

                # switch windows
                driver.switch_to.window('popup')

                popup = Popup(self.driver, self.profile, causa)
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
                except Exception as ex:
                    print(ex)

                try:
                    next_link = driver.find_element(*locator['next_link'])
                    next_link.click()
                    WebDriverWait(driver, settings.WEB_DRIVER_WAIT_TIMEOUT).until(
                        EC.presence_of_element_located(locator['form'])  # takes a tuple as argument so no need for *
                    )
                except Exception as ex:
                    next_link = None
