import os
import requests
import logging
import http.client as http_client
from celery import shared_task
from django.conf import settings
from datetime import datetime

from selenium.webdriver import PhantomJS, Chrome
from bs4 import BeautifulSoup

from main.models import UserProfile

from celery.utils.log import get_task_logger

from main.scraper import Scraper

logger = get_task_logger(__name__)


# http_client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


@shared_task
def run_scraper():
    users = UserProfile.objects.filter(user__is_active=True)
    for profile in users:
        n1 = datetime.now()
        scraper = Scraper(profile)
        scraper.login()
        scraper.init_scraping()
        if not profile.initial_migration_done:
            profile.initial_migration_done = True
            profile.save()
        n2 = datetime.now()
        time = n2 - n1
        print('Done in {} minutes.'.format(round(time.seconds / 60, 2)))


@shared_task
def run_scraper__ok():
    url = 'https://oficinajudicialvirtual.pjud.cl/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Host': 'oficinajudicialvirtual.pjud.cl',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1'
    }
    session = requests.Session()
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
                'username': '15.580.613-3',
                'password': 'leopoldo10'
            }

            print('Login in...')
            login_url = 'https://www.claveunica.gob.cl/accounts/login/'
            resp = session.post(login_url, data=payload, headers={
                'Referer': 'https://www.claveunica.gob.cl/accounts/login/?next={}'.format(auth_url),
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/56.0.2924.87 Safari/537.36',
            })
            if 'https://oficinajudicialvirtual.pjud.cl/session.php' in resp.text:
                print('Login in... OK')
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

                tab_urls = [
                    'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_suprema.php',
                    'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_apelaciones.php',
                    'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_civil.php',
                    'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_laboral.php',
                    'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_penal.php',
                    'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_cobranza.php',
                    'https://oficinajudicialvirtual.pjud.cl/consultaxrut/consultaxrut_familia.php',
                ]

                headers['Referer'] = 'https://oficinajudicialvirtual.pjud.cl/busqueda_por_rut.php'

                payload = {
                    'rut_consulta': '15580613',
                    'dv_consulta': '3',
                    'pagina': '1'
                }
                print('POST {} ...'.format(tab_urls[0]))
                resp = session.post(tab_urls[0], data=payload, headers=headers)
                if './causas/causa_suprema2.php' in resp.text:
                    print('POST {} ...OK'.format(tab_urls[0]))

                    soup = BeautifulSoup(resp.text, 'html.parser')
                    forms = soup.find_all('form', attrs={'action': './causas/causa_suprema2.php'})

                    # TEST:
                    resp = session.post('https://oficinajudicialvirtual.pjud.cl/causas/causa_suprema2.php', data={
                        'rol_causa': '16467',
                        'era_causa': '2015',
                        'codLibro': '1',
                        'codCorte': '1',
                        'gls_libro': 'Civil',
                        'caratulado': 'BASCUÑAN MUÑOZ PATRICIO / ISAPRE MASVIDA S.A.',
                        'gls_estprocesal': 'Fallada',
                        'ubicacion': 'Fallado y devuelto',
                        'gls_corte': 'Corte Suprema',
                        'x': 6,
                        'y': 11,
                    }, headers=headers)

                    resp_text = resp.text.replace('\r', ' ').replace('\n', '')

                    html = '<html><body>{}</body></html>'.format(resp_text)
                    soup = BeautifulSoup(html, 'html.parser')
                    rows = soup.find(id='titTablaSup').parent.find_all('tr')
                    for row in rows:
                        row_content = ' '.join(row.find_all('td')[5].string.split())
                        print(row_content)

                else:
                    print('Error. resp.text: {}'.format(resp.text))

    session.close()

