import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from main.crypto import decrypt
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
            if scraper.try_login(rut, clave):
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
def notifications(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        rut = data['rut']
        clave = data['clave']
        page = data['page']
        try:
            user_profile = UserProfile.objects.get(user__username=rut)

            if clave == decrypt(user_profile.clave):

                items_per_page = settings.NOTIF_API_ITEMS_PER_PAGE
                notification_qs = Notification.objects.filter(profile=user_profile).order_by('-created')
                count = notification_qs.count()
                num_pages = int(count / items_per_page) + 1

                notification_qs = notification_qs[(page - 1) * items_per_page: (page - 1) * items_per_page + items_per_page].values()
                data = [n for n in notification_qs]
                return JsonResponse({
                    'success': True,
                    'data': data,
                    'message': '',
                    'total_records': count,
                    'total_pages': num_pages
                })
            else:
                return JsonResponse({
                    'message': 'Nothing here'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': '{}'.format(e)
            }, status=404)

    else:
        return JsonResponse({
            'message': 'Nothing here'
        })
