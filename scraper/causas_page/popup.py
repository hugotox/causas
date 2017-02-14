from django.conf import settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from main.models import DocSuprema, Causa, DocApelaciones, DocCivil, DocLaboral, DocPenal, DocCobranza, DocFamilia
from main.tasks import send_new_doc_notification
from main.utils import simplify_string
from scraper.core.base_page import BasePage


class PopupLocators(object):
    TABS = (By.ID, 'tabs')
    TABLE = (By.CSS_SELECTOR, '.tablaPop')


class Popup(BasePage):
    def __init__(self, driver, profile, causa):
        super().__init__(driver, '')
        self.profile = profile
        self.causa = causa

    def get_or_create_doc(self, cols):
        tipo_causa = self.causa.type
        created = False
        doc = None
        if tipo_causa == Causa.TYPE_CHOICES_SUPREMA:
            folio = simplify_string(cols[0].text)
            try:
                doc = DocSuprema.objects.get(id='{}__{}'.format(self.causa.id, folio))
            except:
                doc = DocSuprema(
                    id='{}__{}'.format(self.causa.id, folio),
                    causa=self.causa,
                    anio=simplify_string(cols[2].text),
                    fecha=simplify_string(cols[3].text),
                    tipo=simplify_string(cols[4].text),
                    nomenclatura=simplify_string(cols[5].text),
                    descripcion=simplify_string(cols[6].text),
                    salas=simplify_string(cols[7].text)
                )
                doc.save()
                created = True

        elif tipo_causa == Causa.TYPE_CHOICES_APELACIONES:
            folio = simplify_string(cols[2].text)
            try:
                doc = DocApelaciones.objects.get(id='{}__{}'.format(self.causa.id, folio))
            except:
                doc = DocApelaciones(
                    id='{}__{}'.format(self.causa.id, folio),
                    causa=self.causa,
                    tipo=simplify_string(cols[1].text),
                    descripcion=simplify_string(cols[3].text),
                    fecha=simplify_string(cols[4].text),
                    salas=simplify_string(cols[5].text),
                    foja_inicial=simplify_string(cols[6].text)
                )
                doc.save()
                created = True

        elif tipo_causa == Causa.TYPE_CHOICES_CIVIL:
            folio = simplify_string(cols[0].text)
            try:
                doc = DocCivil.objects.get(id='{}__{}'.format(self.causa.id, folio))
            except:
                doc = DocCivil(
                    id='{}__{}'.format(self.causa.id, folio),
                    causa=self.causa,
                    etapa=simplify_string(cols[3].text),
                    tramite=simplify_string(cols[4].text),
                    descripcion=simplify_string(cols[5].text),
                    fecha=simplify_string(cols[6].text),
                    foja=simplify_string(cols[7].text)
                )
                doc.save()
                created = True

        elif tipo_causa == Causa.TYPE_CHOICES_LABORAL:
            doc, created = DocLaboral.objects.get_or_create(
                causa=self.causa,
                tipo=simplify_string(cols[2].text),
                tramite=simplify_string(cols[3].text),
                fecha=simplify_string(cols[4].text),
            )

        elif tipo_causa == Causa.TYPE_CHOICES_PENAL:
            doc, created = DocPenal.objects.get_or_create(
                causa=self.causa,
                tipo=simplify_string(cols[1].text),
                observacion=simplify_string(cols[2].text),
                fecha=simplify_string(cols[3].text),
                estado=simplify_string(cols[4].text),
                cambio_estado=simplify_string(cols[5].text),
            )

        elif tipo_causa == Causa.TYPE_CHOICES_COBRANZA:
            doc, created = DocCobranza.objects.get_or_create(
                causa=self.causa,
                etapa=simplify_string(cols[1].text),
                tramite=simplify_string(cols[2].text),
                desc_tramite=simplify_string(cols[3].text),
                fecha=simplify_string(cols[4].text),
            )

        elif tipo_causa == Causa.TYPE_CHOICES_FAMILIA:
            doc, created = DocFamilia.objects.get_or_create(
                causa=self.causa,
                etapa=simplify_string(cols[2].text),
                tramite=simplify_string(cols[3].text),
                desc_tramite=simplify_string(cols[4].text),
                referencia=simplify_string(cols[5].text),
                fecha=simplify_string(cols[6].text),
            )

        return doc, created

    def check_data(self):
        driver = self.driver

        # wait to make sure the new window is loaded
        WebDriverWait(driver, 10).until(lambda d: d.find_element(*PopupLocators.TABS) is not None)

        # there are 2 tables with the same class, first one is the documents table
        table = driver.find_elements(*PopupLocators.TABLE)[0]

        # first row is heading
        heading = True
        rows = table.find_elements_by_tag_name('tr')

        for row in rows:
            if not heading:
                cols = row.find_elements_by_tag_name('td')
                data = ' - '.join([col.text for col in cols])
                doc, created = self.get_or_create_doc(cols)
                if created:
                    if not self.profile.initial_migration_done:
                        send_new_doc_notification()
                print(data)
            heading = False

        if settings.DRIVER == 'chrome':
            driver.close()  # needed when using Chrome
