from django.conf import settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper.core.base_page import BasePage
from scraper.main_page.locators import MainPageLocators


class MainPage(BasePage):

    def __init__(self, driver, rut, clave):
        super().__init__(driver, 'https://oficinajudicialvirtual.pjud.cl/')
        self.rut = rut
        self.clave = clave

    def login(self):
        driver = self.driver

        # select clave unica
        print('Login...')
        driver.execute_script(MainPageLocators.CLAVE_SCRIPT)

        try:
            WebDriverWait(driver, settings.WEB_DRIVER_WAIT_TIMEOUT).until(
                EC.presence_of_element_located(MainPageLocators.RUT_INPUT)  # takes a tuple as argument so no need for *
            )
        except Exception as ex:
            self.open()
            self.login()

        driver.find_element(*MainPageLocators.RUT_INPUT).send_keys(self.rut)
        driver.find_element(*MainPageLocators.CLAVE_INPUT).send_keys(self.clave)
        driver.find_element(*MainPageLocators.LOGIN_BTN).click()

        print('Login...OK')
