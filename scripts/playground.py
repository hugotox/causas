import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "causas.settings")
import django
django.setup()
import json
from django.conf import settings
from main.models import *
from onesignalsdk import one_signal_sdk


def send_test_notif():
    causa = Causa.objects.get(id='CIV_C_89_2017')
    yo = UserProfile.objects.get(user__username='156844667')

    heading = '{}'.format(causa)
    contents = 'Nueva causa: {}'.format(causa)
    one_signal = one_signal_sdk.OneSignalSdk(settings.ONE_SIGNAL_REST_TOKEN, settings.ONE_SIGNAL_APP_ID)
    one_signal.create_notification(heading=heading,
                                   contents=contents,
                                   player_ids=json.loads(yo.player_id))


yo = UserProfile.objects.get(user__username='156844667')
print(yo.player_id)