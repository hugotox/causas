from celery import shared_task
from django.conf import settings

from main.models import Causa, DocSuprema, DocFamilia, DocCobranza, DocPenal, DocApelaciones, DocCivil, DocLaboral
from onesignalsdk import one_signal_sdk


@shared_task
def send_new_doc_notification(doc_id, causa_type):
    """
    send_email()
    send_SMS()
    send_push()
    save_notification_log()
    """
    doc = None
    causa_type = None

    if causa_type == Causa.TYPE_CHOICES_SUPREMA:
        doc = DocSuprema.objects.get(id=doc_id)
        causa_type = 'Corte Suprema'

    if causa_type == Causa.TYPE_CHOICES_FAMILIA:
        doc = DocFamilia.objects.get(id=doc_id)
        causa_type = 'Familia'

    if causa_type == Causa.TYPE_CHOICES_COBRANZA:
        doc = DocCobranza.objects.get(id=doc_id)
        causa_type = 'Cobranza'

    if causa_type == Causa.TYPE_CHOICES_PENAL:
        doc = DocPenal.objects.get(id=doc_id)
        causa_type = 'Penal'

    if causa_type == Causa.TYPE_CHOICES_APELACIONES:
        doc = DocApelaciones.objects.get(id=doc_id)
        causa_type = 'Corte de Apelaciones'

    if causa_type == Causa.TYPE_CHOICES_CIVIL:
        doc = DocCivil.objects.get(id=doc_id)
        causa_type = 'Civil'

    if causa_type == Causa.TYPE_CHOICES_LABORAL:
        doc = DocLaboral.objects.get(id=doc_id)
        causa_type = 'Laboral'

    if doc and causa_type:

        one_signal = one_signal_sdk.OneSignalSdk(settings.ONE_SIGNAL_REST_TOKEN, settings.ONE_SIGNAL_APP_ID)
        one_signal.create_notification('Actualización causa {}: {}'.format(causa_type, doc.causa_id),
                                       '{}'.format(doc))
