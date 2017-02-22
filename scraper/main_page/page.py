from django.conf import settings
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from main.crypto import decrypt
from scraper.core.base_page import BasePage
from scraper.main_page.locators import MainPageLocators


class MainPage(BasePage):

    def __init__(self, driver, profile=None):
        super().__init__(driver, 'https://oficinajudicialvirtual.pjud.cl/')
        if profile:
            self.rut = profile.user.username
            self.clave = decrypt(profile.clave)

    def login(self):
        self.try_login(self.rut, self.clave)

    def try_login(self, rut, clave):
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

        driver.find_element(*MainPageLocators.RUT_INPUT).send_keys(rut)
        driver.find_element(*MainPageLocators.CLAVE_INPUT).send_keys(clave)
        driver.find_element(*MainPageLocators.LOGIN_BTN).click()

        print('Login...OK')
        return 'https://oficinajudicialvirtual.pjud.cl/frames.php' in driver.current_url
