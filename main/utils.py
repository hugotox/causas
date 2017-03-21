from django.conf import settings
from django.contrib.auth.models import User

from main.crypto import encrypt
from main.models import Causa, UserProfile
from onesignalsdk import one_signal_sdk


def simplify_string(string):
    return string.replace('&nbsp;', '').strip()


def format_rut(rut):
    rut = rut.strip().replace('.', '').replace('-', '')
    rut = rut[::-1]  # reverse string
    rut = '{}-{}.{}.{}'.format(rut[0], rut[1:4], rut[4:7], rut[7:])
    rut = rut[::-1]
    return rut


def send_new_doc_notification(doc):
    """
    send_email()
    send_SMS()
    send_push()
    save_notification_log()
    """
    causa_type = doc.causa.type

    if causa_type == Causa.TYPE_CHOICES_SUPREMA:
        causa_type = 'Corte Suprema'

    elif causa_type == Causa.TYPE_CHOICES_FAMILIA:
        causa_type = 'Familia'

    elif causa_type == Causa.TYPE_CHOICES_COBRANZA:
        causa_type = 'Cobranza'

    elif causa_type == Causa.TYPE_CHOICES_PENAL:
        causa_type = 'Penal'

    elif causa_type == Causa.TYPE_CHOICES_APELACIONES:
        causa_type = 'Corte de Apelaciones'

    elif causa_type == Causa.TYPE_CHOICES_CIVIL:
        causa_type = 'Civil'

    elif causa_type == Causa.TYPE_CHOICES_LABORAL:
        causa_type = 'Laboral'

    if not settings.DEBUG and doc and causa_type:
        one_signal = one_signal_sdk.OneSignalSdk(settings.ONE_SIGNAL_REST_TOKEN, settings.ONE_SIGNAL_APP_ID)
        one_signal.create_notification(heading='{}: {}'.format(causa_type, doc.causa),
                                       contents='{}'.format(doc),
                                       player_ids=[doc.causa.user.player_id])


def create_user(username, password, player_id):
    user = User.objects.create(username=username)
    up = UserProfile.objects.create(user=user, clave=encrypt(password), player_id=player_id)
    return up
