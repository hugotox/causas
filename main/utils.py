from django.conf import settings
from django.contrib.auth.models import User

from main.crypto import encrypt
from main.models import Causa, UserProfile, Notification
from onesignalsdk import one_signal_sdk


def simplify_string(string):
    try:
        return string.replace('&nbsp;', '').strip()
    except:
        return ''


def format_rut(rut):
    rut = rut.strip().replace('.', '').replace('-', '')
    rut = rut[::-1]  # reverse string
    rut = '{}-{}.{}.{}'.format(rut[0], rut[1:4], rut[4:7], rut[7:])
    rut = rut[::-1]
    return rut


def send_new_doc_notification(doc):

    if not settings.DEBUG and doc and doc.causa.type:
        heading = '{}'.format(doc.causa)
        contents = '{}'.format(doc)
        one_signal = one_signal_sdk.OneSignalSdk(settings.ONE_SIGNAL_REST_TOKEN, settings.ONE_SIGNAL_APP_ID)
        one_signal.create_notification(heading=heading,
                                       contents=contents,
                                       player_ids=doc.causa.user.player_id)
        Notification.objects.create(
            profile=doc.causa.user,
            heading=heading,
            contents=contents,
            player_id=doc.causa.user.player_id,
            document_type=doc.causa.type,
            document_id=doc.id
        )


def create_user(username, password, player_id):
    user = User.objects.create(username=username)
    up = UserProfile.objects.create(user=user, clave=encrypt(password), player_id=player_id)
    return up
