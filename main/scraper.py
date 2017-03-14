import requests
import re
from bs4 import BeautifulSoup

from main.crypto import decrypt
from main.models import Causa, DocSuprema
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

    }

    def __init__(self, profile):
        self.profile = profile
        self.session = requests.Session()
        self.rut_consulta = self.profile.user.username.strip().replace('.', '').replace('-', '')[0:-1]
        self.dv_consulta = self.profile.user.username.strip().replace('.', '').replace('-', '')[-1]
        self.username = format_rut(self.profile.user.username)
        self.clave = decrypt(self.profile.clave)

    def login(self):
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
                    'username': self.username,
                    'password': self.clave
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
                else:
                    raise Exception('Unable to log in. {}'.format(resp.text))
            else:
                raise Exception('Unable to find csrfmiddlewaretoken')

        else:
            raise Exception('Unable to load {}'.format(url))

    def _get_total_records(self, text):
        session = self.session
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
                scrape_documents(causa)
            return resp.text
        else:
            raise Exception('Unable to find Suprema forms')

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
            causa_id = '{}-{}'.format(data['rol_causa'], data['era_causa'])
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
                        folio = tds[0].string.strip()  # TODO crashing here
                        doc_id = '{}__{}'.format(causa_id, folio)
                        created = False
                        try:
                            doc_obj = DocSuprema.objects.get(id=doc_id)
                        except:
                            doc_obj = DocSuprema(
                                id=doc_id,
                                causa=causa_obj,
                                anio=tds[2].string.strip(),
                                fecha=tds[3].string.strip(),
                                tipo=tds[4].string.strip(),
                                nomenclatura=tds[5].string.strip(),
                                descripcion=tds[6].string.strip(),
                                salas=tds[7].string.strip()
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
            raise Exception('Unable to find causa documents')

    def scrape_suprema(self):
        # I need to post page 1 to know the total pages. Then loop starts from page 2
        resp_text = self.post_causa_type('suprema', 1, self.scrape_suprema_document)

        # find total record to calculate total pages
        total_records = self._get_total_records(resp_text)
        print('Total records: {}'.format(total_records))
        total_pages = int(total_records / 10 + 1)
        print('Total pages: {}'.format(total_pages))
        if total_pages > 1:
            for page in range(2, total_pages + 1):
                self.post_causa_type('suprema', page, self.scrape_suprema_document)

    def scrape_apelaciones(self):
        pass

    def scrape_civil(self):
        pass

    def scrape_laboral(self):
        pass

    def scrape_penal(self):
        pass

    def scrape_cobranza(self):
        pass

    def scrape_familia(self):
        pass

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

        self.scrape_suprema()
        self.scrape_apelaciones()
        self.scrape_civil()
        self.scrape_laboral()
        self.scrape_penal()
        self.scrape_cobranza()
        self.scrape_familia()

        session.close()
