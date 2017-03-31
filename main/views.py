import json

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from main.models import UserProfile, Notification
from main.scraper import Scraper
from main.utils import create_user


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        rut = data['rut']
        clave = data['clave']
        player_id = data['playerId']

        # if existing user then do not call external login
        try:
            user_profile = UserProfile.objects.get(user__username=rut)
            if player_id:
                if user_profile.player_id:
                    player_id_list = json.loads(user_profile.player_id)
                    if player_id not in player_id_list:
                        player_id_list.append(player_id)
                    user_profile.player_id = json.dumps(player_id_list)
                else:
                    user_profile.player_id = json.dumps([player_id])
                user_profile.save()  # always save player_id because user can switch phone
            return JsonResponse({
                'success': True,
                'message': ''
            })
        except Exception as ex:
            scraper = Scraper()
            if True:  # scraper.try_login(rut, clave):
                # create the user only if the external login was successful
                create_user(
                    username=rut,
                    password=clave,
                    player_id=json.dumps([player_id]))  # saves username, password, clave and player_id

                return JsonResponse({
                    'success': True,
                    'message': ''
                })

            else:
                return JsonResponse({
                    'success': False,
                    'message': 'RUN o clave incorrecta.'
                })
    else:
        return JsonResponse({
            'message': 'Nothing here'
        })


@csrf_exempt
def notifications(request, rut):
    try:
        notifications_qs = Notification.objects.filter(profile__user__username=rut).values()
        data = [n for n in notifications_qs]
        return JsonResponse({
            'success': True,
            'data': data,
            'message': ''
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': '{}'.format(e)
        }, status=404)
