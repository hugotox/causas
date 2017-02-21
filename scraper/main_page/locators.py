from selenium.webdriver.common.by import By


class MainPageLocators(object):

    CLAVE_SCRIPT = 'AutenticaCUnica()'
    RUT_INPUT = (By.ID, 'inputUsuario')
    CLAVE_INPUT = (By.ID, 'inputPassword')
    LOGIN_BTN = (By.CSS_SELECTOR, '.btn-primary')
    LOGGEDIN_INPUT = (By.ID, 'usuario_conectado')
