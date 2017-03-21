import requests
import re
from bs4 import BeautifulSoup

from main.crypto import decrypt
from main.models import Causa, DocSuprema, DocApelaciones, DocCivil, DocLaboral, DocPenal, DocCobranza, DocFamilia
from main.utils import format_rut, send_new_doc_notification


class Scraper:

    SCRAPER_HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like '
                      'Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Host': 'oficinajudicialvirtual.pjud.cl',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://oficinajudicialvirtual.pjud.cl/busqueda_por_rut.php'
    }

    CAUSA_TYPES = {
        'suprema': {
            'url': 'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_suprema.php',
            'detail': 'https://oficinajudicialvirtual.pjud.cl/causas/causa_suprema2.php',
            'locator': './causas/causa_suprema2.php'
        },
        'apelaciones': {
            'url': 'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_apelaciones.php',
            'detail': 'https://oficinajudicialvirtual.pjud.cl/causas/causa_corte2.php',
            'locator': './causas/causa_corte2.php'
        },
        'civil': {
            'url': 'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_civil.php',
            'detail': 'https://oficinajudicialvirtual.pjud.cl/causas/causaCivil2.php',
            'locator': './causas/causaCivil2.php'
        },
        'laboral': {
            'url': 'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_laboral.php',
            'detail': 'https://oficinajudicialvirtual.pjud.cl/causas/causa_laboral_reformado2.php',
            'locator': './causas/causa_laboral_reformado2.php'
        },
        'penal': {
            'url': 'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_penal.php',
            'detail': 'https://oficinajudicialvirtual.pjud.cl/causas/causa_penal2.php',
            'locator': './causas/causa_penal2.php'
        },
        'cobranza': {
            'url': 'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_cobranza.php',
            'detail': 'https://oficinajudicialvirtual.pjud.cl/causas/causa_cobranza2.php',
            'locator': './causas/causa_cobranza2.php'
        },
        'familia': {
            'url': 'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_familia.php',
            'detail': 'https://oficinajudicialvirtual.pjud.cl/causas/causaFamilia2.php',
            'locator': './causas/causaFamilia2.php'
        },
    }

    def __init__(self, profile=None):
        self.session = requests.Session()
        if profile:
            self.profile = profile
            self.rut_consulta = self.profile.user.username.strip().replace('.', '').replace('-', '')[0:-1]
            self.dv_consulta = self.profile.user.username.strip().replace('.', '').replace('-', '')[-1]
            self.username = format_rut(self.profile.user.username)
            self.clave = decrypt(self.profile.clave)

    def login(self):
        self.try_login(self.username, self.clave)

    def try_login(self, rut, clave):
        url = 'https://oficinajudicialvirtual.pjud.cl/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.87 Safari/537.36',
            'Host': 'oficinajudicialvirtual.pjud.cl',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1'
        }
        session = self.session
        print('Loading {} ...'.format(url))
        resp = session.get(url, headers=headers)
        print('Loading {} ...OK'.format(url))

        if 'https://www.claveunica.gob.cl/openid/authorize' in resp.text:
            idx1 = resp.text.index('https://www.claveunica.gob.cl/openid/authorize')
            idx2 = idx1
            current = ''
            while current != "'":
                idx2 += 1
                current = resp.text[idx2]

            auth_url = resp.text[idx1:idx2]
            print('Loading {} ...'.format(auth_url))

            resp = session.get(auth_url, headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-US,en;q=0.8',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'referer': 'https://oficinajudicialvirtual.pjud.cl/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/56.0.2924.87 Safari/537.36',
            })

            print('Loading {} ... OK'.format(auth_url))

            soup = BeautifulSoup(resp.text, 'html.parser')
            csrf_input = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})

            if csrf_input:
                payload = {
                    'csrfmiddlewaretoken': csrf_input.attrs['value'],
                    'next': soup.find('input', attrs={'name': 'next'}).attrs['value'],
                    'nombre_app': 'PJUD',
                    'retorno': 'https://oficinajudicialvirtual.pjud.cl/claveunica/return.php',
                    'username': format_rut(rut),
                    'password': clave
                }

                print('Login in... {}'.format(payload))
                login_url = 'https://www.claveunica.gob.cl/accounts/login/'
                resp = session.post(login_url, data=payload, headers={
                    'Referer': 'https://www.claveunica.gob.cl/accounts/login/?next={}'.format(auth_url),
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like '
                                  'Gecko) Chrome/56.0.2924.87 Safari/537.36',
                })
                if 'https://oficinajudicialvirtual.pjud.cl/session.php' in resp.text:
                    print('Login in... OK')
                    return True
                else:
                    # raise Exception('Unable to log in. {}'.format(resp.text))
                    return False
            else:
                # raise Exception('Unable to find csrfmiddlewaretoken')
                return False

        else:
            # raise Exception('Unable to load {}'.format(url))
            return False

    def _get_total_records(self, text):
        regex = re.compile('de un total de \d+ registros')
        line = regex.search(text)
        if line:
            total_records = re.findall(r'\d+', line.group())
            if total_records:
                total_records = int(total_records[0])
                return total_records
            else:
                raise Exception('Unable to find total records')
        else:
            raise Exception('Unable to find total records regex')

    def post_causa_type(self, causa_type, page, scrape_documents):
        """Opens the causas list based on causa type and the pagination number. Then loops through all causas
        and calls the document scraper for each one"""
        url = Scraper.CAUSA_TYPES[causa_type]['url']
        locator = Scraper.CAUSA_TYPES[causa_type]['locator']
        session = self.session
        payload = {
            'rut_consulta': self.rut_consulta,
            'dv_consulta': self.dv_consulta,
            'pagina': page
        }
        print('POST {} ... Page: {}'.format(url, page))
        resp = session.post(url, data=payload, headers=Scraper.SCRAPER_HEADERS)
        if locator in resp.text:
            print('POST {} ...OK'.format(url))
            soup = BeautifulSoup(resp.text, 'html.parser')
            causas = soup.find_all('form', attrs={'action': locator})
            for causa in causas:
                if 'causa not closed':  # TODO <-- this
                    scrape_documents(causa)
            return resp.text
        else:
            print('Unable to find {} forms'.format(causa_type))

    def scrape_suprema_document(self, causa):
        """Opens the detail of a causa"""
        session = self.session
        url = Scraper.CAUSA_TYPES['suprema']['detail']
        data = {}
        for input_elm in causa.find_all('input'):
            if 'name' in input_elm.attrs.keys() and 'value' in input_elm.attrs.keys():
                data[input_elm.attrs['name']] = input_elm.attrs['value']

        causa_obj = None
        causa_id = None
        if 'rol_causa' in data.keys() and 'era_causa' in data.keys():
            causa_id = '1-{}-{}'.format(data['rol_causa'], data['era_causa'])  # cod corte suprema = 1
            try:
                causa_obj = Causa.objects.get(id=causa_id)
            except Exception as ex:
                causa_obj = Causa(id=causa_id, user=self.profile, type=Causa.TYPE_CHOICES_SUPREMA, archived=False,
                                  caratulado=data['caratulado'])
                causa_obj.save()

        if causa_obj and causa_id:
            print(causa_obj)
            # Open causa details:
            resp = session.post(url, data=data, headers=Scraper.SCRAPER_HEADERS)
            if 'Recurso Corte Suprema' in resp.text:
                resp_text = resp.text.replace('\r', ' ').replace('\n', '')
                html = '<html><body>{}</body></html>'.format(resp_text)
                soup = BeautifulSoup(html, 'html.parser')
                rows = soup.find(id='titTablaSup').parent.find_all('tr')
                header = True
                for row in rows:
                    if not header:  # skip the header row
                        tds = row.find_all('td')
                        iddoc_input = row.find('input', attrs={'name': 'iddoc'})
                        if iddoc_input:
                            doc_id = '{}__{}'.format(causa_id, iddoc_input.attrs['value'])
                            created = False
                            try:
                                doc_obj = DocSuprema.objects.get(id=doc_id)
                            except:
                                doc_obj = DocSuprema(
                                    id=doc_id,
                                    causa=causa_obj,
                                    anio=tds[2].string,
                                    fecha=tds[3].string,
                                    tipo=tds[4].string,
                                    nomenclatura=tds[5].string,
                                    descripcion=tds[6].string,
                                    salas=tds[7].string
                                )
                                doc_obj.save()
                                created = True

                            if created:
                                if self.profile.initial_migration_done:
                                    print('Sending notification: {}'.format(doc_obj))
                                    send_new_doc_notification(doc_obj)

                            print(doc_obj)

                    else:
                        header = False
        else:
            raise Exception('Unable to find suprema documents')

    def scrape_apelaciones_document(self, causa):
        """Opens the detail of a causa. `causa` is the soup form element"""
        session = self.session
        url = Scraper.CAUSA_TYPES['apelaciones']['detail']
        data = {}
        for input_elm in causa.find_all('input'):
            if 'name' in input_elm.attrs.keys() and 'value' in input_elm.attrs.keys():
                data[input_elm.attrs['name']] = input_elm.attrs['value']

        causa_obj = None
        causa_id = None
        if 'rol_causa' in data.keys() and 'era_causa' in data.keys():
            causa_id = '50-{}-{}'.format(data['rol_causa'], data['era_causa'])  # cod corte apelaciones = 50
            tr = causa.parent.parent
            tds = tr.find_all('td')
            caratulado = tds[3].string
            try:
                causa_obj = Causa.objects.get(id=causa_id)
            except Exception as ex:
                causa_obj = Causa(id=causa_id, user=self.profile, type=Causa.TYPE_CHOICES_APELACIONES, archived=False,
                                  caratulado=caratulado)
                causa_obj.save()

        if causa_obj and causa_id:
            print(causa_obj)
            # Open causa details:
            resp = session.post(url, data=data, headers=Scraper.SCRAPER_HEADERS)
            if 'Recurso Corte de Apelaciones' in resp.text:
                resp_text = resp.text.replace('\r', ' ').replace('\n', '')
                html = '<html><body>{}</body></html>'.format(resp_text)
                soup = BeautifulSoup(html, 'html.parser')
                rows = soup.find(id='titTablaApeGrid').parent.find_all('tr')
                header = True
                for row in rows:
                    if not header:  # skip the header row
                        tds = row.find_all('td')
                        if tds[2].string and tds[2].string.strip() != '':
                            doc_id = '{}__{}'.format(causa_id, tds[2].string.strip())
                            created = False
                            try:
                                doc_obj = DocApelaciones.objects.get(id=doc_id)
                            except:
                                doc_obj = DocApelaciones(
                                    id=doc_id,
                                    causa=causa_obj,
                                    tipo=tds[1].string,
                                    descripcion=tds[3].string,
                                    fecha=tds[4].string,
                                    salas=tds[5].string,
                                    foja_inicial=tds[6].string
                                )
                                doc_obj.save()
                                created = True

                            if created:
                                if self.profile.initial_migration_done:
                                    print('Sending notification: {}'.format(doc_obj))
                                    send_new_doc_notification(doc_obj)

                            print(doc_obj)

                    else:
                        header = False
        else:
            raise Exception('Unable to find apelaciones documents')

    def scrape_civil_document(self, causa):
        """Opens the detail of a causa. `causa` is the soup form element"""
        session = self.session
        url = Scraper.CAUSA_TYPES['civil']['detail']
        data = {}
        for input_elm in causa.find_all('input'):
            if 'name' in input_elm.attrs.keys() and 'value' in input_elm.attrs.keys():
                data[input_elm.attrs['name']] = input_elm.attrs['value']

        causa_obj = None
        causa_id = None
        if 'rol' in data.keys() and 'ano' in data.keys():
            causa_id = 'C-{}-{}'.format(data['rol'], data['ano'])  # cod civil = C
            tr = causa.parent.parent
            tds = tr.find_all('td')
            caratulado = tds[3].string
            try:
                causa_obj = Causa.objects.get(id=causa_id)
            except Exception as ex:
                causa_obj = Causa(id=causa_id, user=self.profile, type=Causa.TYPE_CHOICES_CIVIL, archived=False,
                                  caratulado=caratulado)
                causa_obj.save()

        if causa_obj and causa_id:
            print(causa_obj)
            # Open causa details:
            resp = session.post(url, data=data, headers=Scraper.SCRAPER_HEADERS)
            if 'Causa Civil' in resp.text:
                resp_text = resp.text.replace('\r', ' ').replace('\n', '')
                html = '<html><body>{}</body></html>'.format(resp_text)
                soup = BeautifulSoup(html, 'html.parser')
                rows = soup.find(id='titTablaCiv').parent.parent.find_all('tr')  # double parent becaouse this one has header tr inside <thead>
                header = True
                for row in rows:
                    if not header:  # skip the header row
                        tds = row.find_all('td')
                        if tds[0].string and tds[0].string.strip() != '':
                            doc_id = '{}__{}'.format(causa_id, tds[2].string.strip())  # id = causa_id__folio
                            created = False
                            try:
                                doc_obj = DocCivil.objects.get(id=doc_id)
                            except:
                                doc_obj = DocCivil(
                                    id=doc_id,
                                    causa=causa_obj,
                                    etapa=tds[3].string,
                                    tramite=tds[4].string,
                                    descripcion=tds[5].string,
                                    fecha=tds[6].string,
                                    foja=tds[7].string
                                )
                                doc_obj.save()
                                created = True

                            if created:
                                if self.profile.initial_migration_done:
                                    print('Sending notification: {}'.format(doc_obj))
                                    send_new_doc_notification(doc_obj)

                            print(doc_obj)

                    else:
                        header = False
        else:
            raise Exception('Unable to find civil documents')

    def scrape_laboral_document(self, causa):
        """Opens the detail of a causa. `causa` is the soup form element"""
        session = self.session
        url = Scraper.CAUSA_TYPES['laboral']['detail']
        data = {}
        for input_elm in causa.find_all('input'):
            if 'name' in input_elm.attrs.keys() and 'value' in input_elm.attrs.keys():
                data[input_elm.attrs['name']] = input_elm.attrs['value']

        causa_obj = None
        causa_id = None
        if 'rol_causa' in data.keys() and 'era_causa' in data.keys() and 'cod_tribunal' in data.keys():
            causa_id = '{}-{}-{}'.format(data['cod_tribunal'], data['rol_causa'], data['era_causa'])
            tr = causa.parent.parent
            tds = tr.find_all('td')
            caratulado = tds[3].string
            try:
                causa_obj = Causa.objects.get(id=causa_id)
            except Exception as ex:
                causa_obj = Causa(id=causa_id, user=self.profile, type=Causa.TYPE_CHOICES_LABORAL, archived=False,
                                  caratulado=caratulado)
                causa_obj.save()

        if causa_obj and causa_id:
            print(causa_obj)
            # Open causa details:
            resp = session.post(url, data=data, headers=Scraper.SCRAPER_HEADERS)
            if 'Causa Laboral' in resp.text:
                resp_text = resp.text.replace('\r', ' ').replace('\n', '')
                html = '<html><body>{}</body></html>'.format(resp_text)
                soup = BeautifulSoup(html, 'html.parser')
                rows = soup.find(id='titTablaLab').parent.find_all('tr')
                header = True
                for row in rows:
                    if not header:  # skip the header row
                        doc_data = {}
                        for doc_input in row.find_all('input'):
                            try:
                                doc_data[doc_input.attrs['name']] = doc_input.attrs['value']
                            except:
                                pass
                        doc_keys = doc_data.keys()
                        doc_id = None
                        if 'crr_docfallo' in doc_keys and 'cod_tribunal' in doc_keys and 'tip_doc' in doc_keys and 'est_firma' in doc_keys:
                            doc_id = '{}-{}-{}-{}'.format(doc_data['cod_tribunal'], doc_data['crr_docfallo'], doc_data['tip_doc'], doc_data['est_firma'])
                        tds = row.find_all('td')
                        if doc_id:
                            created = False
                            try:
                                doc_obj = DocLaboral.objects.get(id=doc_id)
                            except:
                                doc_obj = DocLaboral(
                                    id=doc_id,
                                    causa=causa_obj,
                                    tipo=tds[1].string,
                                    tramite=tds[2].string,
                                    fecha=tds[3].string,
                                )
                                doc_obj.save()
                                created = True

                            if created:
                                if self.profile.initial_migration_done:
                                    print('Sending notification: {}'.format(doc_obj))
                                    send_new_doc_notification(doc_obj)

                            print(doc_obj)

                    else:
                        header = False
        else:
            raise Exception('Unable to find laboral documents')

    def scrape_penal_document(self, causa):
        """Opens the detail of a causa. `causa` is the soup form element"""
        session = self.session
        url = Scraper.CAUSA_TYPES['penal']['detail']
        data = {}
        for input_elm in causa.find_all('input'):
            if 'name' in input_elm.attrs.keys() and 'value' in input_elm.attrs.keys():
                data[input_elm.attrs['name']] = input_elm.attrs['value']

        causa_obj = None
        causa_id = None
        if 'rol_causa' in data.keys() and 'era_causa' in data.keys() and 'cod_tribunal' in data.keys():
            causa_id = '{}-{}-{}'.format(data['cod_tribunal'], data['rol_causa'], data['era_causa'])
            tr = causa.parent.parent
            tds = tr.find_all('td')
            caratulado = tds[4].string
            try:
                causa_obj = Causa.objects.get(id=causa_id)
            except Exception as ex:
                causa_obj = Causa(id=causa_id, user=self.profile, type=Causa.TYPE_CHOICES_PENAL, archived=False,
                                  caratulado=caratulado)
                causa_obj.save()

        if causa_obj and causa_id:
            print(causa_obj)
            # Open causa details:
            resp = session.post(url, data=data, headers=Scraper.SCRAPER_HEADERS)
            if 'Causa Penal' in resp.text:
                resp_text = resp.text.replace('\r', ' ').replace('\n', '')
                html = '<html><body>{}</body></html>'.format(resp_text)
                soup = BeautifulSoup(html, 'html.parser')
                rows = soup.find(id='titTablaPen').parent.find_all('tr')
                header = True
                for row in rows:
                    if not header:  # skip the header row
                        doc_data = {}
                        for doc_input in row.find_all('input'):
                            try:
                                doc_data[doc_input.attrs['name']] = doc_input.attrs['value']
                            except:
                                pass
                        doc_keys = doc_data.keys()
                        doc_id = None
                        if 'tipDoc' in doc_keys and 'valor' in doc_keys:
                            doc_id = 'P-{}-{}'.format(doc_data['tipDoc'], doc_data['valor'])
                        tds = row.find_all('td')
                        if doc_id:
                            created = False
                            try:
                                doc_obj = DocPenal.objects.get(id=doc_id)
                            except:
                                doc_obj = DocPenal(
                                    id=doc_id,
                                    causa=causa_obj,
                                    tipo=tds[1].string,
                                    observacion=tds[2].string,
                                    fecha=tds[3].string,
                                    estado=tds[4].string,
                                    cambio_estado=tds[5].string,
                                )
                                doc_obj.save()
                                created = True

                            if created:
                                if self.profile.initial_migration_done:
                                    print('Sending notification: {}'.format(doc_obj))
                                    send_new_doc_notification(doc_obj)

                            print(doc_obj)

                    else:
                        header = False
        else:
            raise Exception('Unable to find penal documents')

    def scrape_cobranza_document(self, causa):
        """Opens the detail of a causa. `causa` is the soup form element"""
        session = self.session
        url = Scraper.CAUSA_TYPES['cobranza']['detail']
        data = {}
        for input_elm in causa.find_all('input'):
            if 'name' in input_elm.attrs.keys() and 'value' in input_elm.attrs.keys():
                data[input_elm.attrs['name']] = input_elm.attrs['value']
        causa_obj = None
        causa_id = None

        data_keys = data.keys()

        if 'cod_tribunal' in data_keys and 'rol_causa' in data_keys and 'era_causa' in data_keys:
            causa_id = '{}-{}-{}'.format(data['cod_tribunal'], data['rol_causa'], data['era_causa'])
            tr = causa.parent.parent
            tds = tr.find_all('td')
            caratulado = tds[3].string
            try:
                causa_obj = Causa.objects.get(id=causa_id)
            except Exception as ex:
                causa_obj = Causa(id=causa_id, user=self.profile, type=Causa.TYPE_CHOICES_COBRANZA, archived=False,
                                  caratulado=caratulado)
                causa_obj.save()

        if causa_obj and causa_id:
            print(causa_obj)
            # Open causa details:
            resp = session.post(url, data=data, headers=Scraper.SCRAPER_HEADERS)
            if 'Causa Cobranza' in resp.text:
                resp_text = resp.text.replace('\r', ' ').replace('\n', '')
                html = '<html><body>{}</body></html>'.format(resp_text)
                soup = BeautifulSoup(html, 'html.parser')
                rows = soup.find(id='titTablaCob').parent.find_all('tr')
                header = True
                for row in rows:
                    if not header:  # skip the header row
                        doc_data = {}
                        for doc_input in row.find_all('input'):
                            try:
                                doc_data[doc_input.attrs['name']] = doc_input.attrs['value']
                            except:
                                pass
                        doc_keys = doc_data.keys()
                        doc_id = None
                        if 'cod_tribunal' in doc_keys and 'crr_iddocumento' in doc_keys:
                            doc_id = 'COB-{}-{}'.format(doc_data['cod_tribunal'], doc_data['crr_iddocumento'])
                        tds = row.find_all('td')
                        if doc_id:
                            created = False
                            try:
                                doc_obj = DocCobranza.objects.get(id=doc_id)
                            except:
                                doc_obj = DocCobranza(
                                    id=doc_id,
                                    causa=causa_obj,
                                    etapa=tds[1].string,
                                    tramite=tds[2].string,
                                    desc_tramite=tds[3].string,
                                    fecha=tds[4].string,
                                )
                                doc_obj.save()
                                created = True

                            if created:
                                if self.profile.initial_migration_done:
                                    print('Sending notification: {}'.format(doc_obj))
                                    send_new_doc_notification(doc_obj)

                            print(doc_obj)

                    else:
                        header = False
        else:
            raise Exception('Unable to find cobranza documents')

    def scrape_familia_document(self, causa):
        """Opens the detail of a causa. `causa` is the soup form element"""
        session = self.session
        url = Scraper.CAUSA_TYPES['familia']['detail']
        data = {}
        for input_elm in causa.find_all('input'):
            if 'name' in input_elm.attrs.keys() and 'value' in input_elm.attrs.keys():
                data[input_elm.attrs['name']] = input_elm.attrs['value']
        causa_id = '-'.join(data.values())  # TODO: use this kind of id for all causas
        tr = causa.parent.parent
        tds = tr.find_all('td')
        caratulado = tds[3].string
        try:
            causa_obj = Causa.objects.get(id=causa_id)
        except Exception as ex:
            causa_obj = Causa(id=causa_id, user=self.profile, type=Causa.TYPE_CHOICES_FAMILIA, archived=False,
                              caratulado=caratulado)
            causa_obj.save()

        if causa_obj and causa_id:
            print(causa_obj)
            # Open causa details:
            resp = session.post(url, data=data, headers=Scraper.SCRAPER_HEADERS)
            if 'Causa Familia' in resp.text:
                resp_text = resp.text.replace('\r', ' ').replace('\n', '')
                html = '<html><body>{}</body></html>'.format(resp_text)
                soup = BeautifulSoup(html, 'html.parser')
                rows = soup.find(id='titTablaFam').parent.find_all('tr')
                header = True
                for row in rows:
                    if not header:  # skip the header row
                        link = row.find('a')
                        if link and 'onclick' in link.attrs:
                            onclick = link.attrs['onclick']  # E.g "vvbbFF('Resolución',3,59987979,0);"
                            doc_id = onclick.replace('vvbbFF(', '').replace(');', '').replace(',', '-').replace("'", '')
                            tds = row.find_all('td')
                            if doc_id:
                                created = False
                                try:
                                    doc_obj = DocFamilia.objects.get(id=doc_id)
                                except:
                                    doc_obj = DocFamilia(
                                        id=doc_id,
                                        causa=causa_obj,
                                        etapa=tds[2].string,
                                        tramite=tds[3].string,
                                        desc_tramite=tds[4].string,
                                        referencia=tds[5].string,
                                        fecha=tds[6].string,
                                    )
                                    doc_obj.save()
                                    created = True

                                if created:
                                    if self.profile.initial_migration_done:
                                        print('Sending notification: {}'.format(doc_obj))
                                        send_new_doc_notification(doc_obj)

                                print(doc_obj)

                    else:
                        header = False
        else:
            raise Exception('Unable to find familia documents')

    def scrape_causas(self, type, doc_scraper):
        # I need to post page 1 to know the total pages. Then loop starts from page 2
        resp_text = self.post_causa_type(type, 1, doc_scraper)

        if resp_text:
            # find total record to calculate total pages
            total_records = self._get_total_records(resp_text)
            print('Total records: {}'.format(total_records))
            total_pages = int(total_records / 10 + 1)
            print('Total pages: {}'.format(total_pages))
            if total_pages > 1:
                for page in range(2, total_pages + 1):
                    self.post_causa_type(type, page, doc_scraper)

    def init_scraping(self):
        session = self.session

        session.get('https://oficinajudicialvirtual.pjud.cl/session.php')

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like '
                          'Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': 'https://oficinajudicialvirtual.pjud.cl/',
            'Host': 'oficinajudicialvirtual.pjud.cl',
            'Upgrade-Insecure-Requests': '1'
        }

        url = 'https://oficinajudicialvirtual.pjud.cl/busqueda_por_rut.php'

        print('Loading {} ...'.format(url))
        session.get(url, headers=headers)
        print('Loading {} ...OK'.format(url))

        # self.scrape_causas('suprema', self.scrape_suprema_document)
        # self.scrape_causas('apelaciones', self.scrape_apelaciones_document)
        # self.scrape_causas('civil', self.scrape_civil_document)
        # self.scrape_causas('laboral', self.scrape_laboral_document)
        # self.scrape_causas('penal', self.scrape_penal_document)
        # self.scrape_causas('cobranza', self.scrape_cobranza_document)
        # self.scrape_causas('familia', self.scrape_familia_document)

        session.close()
