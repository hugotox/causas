from django.conf import settings

from main.models import Causa
from onesignalsdk import one_signal_sdk


def simplify_string(string):
    return string.replace('&nbsp;', '').strip()


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

    if causa_type == Causa.TYPE_CHOICES_FAMILIA:
        causa_type = 'Familia'

    if causa_type == Causa.TYPE_CHOICES_COBRANZA:
        causa_type = 'Cobranza'

    if causa_type == Causa.TYPE_CHOICES_PENAL:
        causa_type = 'Penal'

    if causa_type == Causa.TYPE_CHOICES_APELACIONES:
        causa_type = 'Corte de Apelaciones'

    if causa_type == Causa.TYPE_CHOICES_CIVIL:
        causa_type = 'Civil'

    if causa_type == Causa.TYPE_CHOICES_LABORAL:
        causa_type = 'Laboral'

    if doc and causa_type:
        one_signal = one_signal_sdk.OneSignalSdk(settings.ONE_SIGNAL_REST_TOKEN, settings.ONE_SIGNAL_APP_ID)
        one_signal.create_notification(heading='{}: {}'.format(causa_type, doc.causa),
                                       contents='{}'.format(doc))
