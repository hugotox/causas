from selenium.webdriver.common.by import By


class CausasPageLocators(object):
    FORM_SUPREMA     = "//form[@action='./causas/causa_suprema2.php']"
    FORM_APELACIONES = "//form[@action='./causas/causa_corte2.php']"
    FORM_CIVIL       = "//form[@action='./causas/causaCivil2.php']"
    FORM_LABORAL     = "//form[@action='./causas/causa_laboral_reformado2.php']"
    FORM_PENAL       = "//form[@action='./causas/causa_penal2.php']"
    FORM_COBRANZA    = "//form[@action='./causas/causa_cobranza2.php']"
    FORM_FAMILIA     = "//form[@action='./causas/causaFamilia2.php']"

    # every tab has 10 rows of forms, all of them with the same action
    FORMS_XPATHS = [
        {
            'form': (By.XPATH, FORM_SUPREMA),
            'next_link': (By.ID, 'suprema_siguiente'),
            'tab': (By.ID, 'ui-id-1'),
        },
        {
            'form': (By.XPATH, FORM_APELACIONES),
            'next_link': (By.ID, 'corte_siguiente'),
            'tab': (By.ID, 'ui-id-2'),
        },
        {
            'form': (By.XPATH, FORM_CIVIL),
            'next_link': (By.ID, 'civil_siguiente'),
            'tab': (By.ID, 'ui-id-3'),
        },
        {
            'form': (By.XPATH, FORM_LABORAL),
            'next_link': (By.ID, 'laboral_siguiente'),
            'tab': (By.ID, 'ui-id-4'),
        },
        {
            'form': (By.XPATH, FORM_PENAL),
            'next_link': (By.ID, 'penal_siguiente'),
            'tab': (By.ID, 'ui-id-5'),
        },
        {
            'form': (By.XPATH, FORM_COBRANZA),
            'next_link': (By.ID, 'cobranza_siguiente'),
            'tab': (By.ID, 'ui-id-6'),
        },
        {
            'form': (By.XPATH, FORM_FAMILIA),
            'next_link': (By.ID, 'familia_siguiente'),
            'tab': (By.ID, 'ui-id-7'),
        }
    ]