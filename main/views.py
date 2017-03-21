import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from main.models import UserProfile
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
            return JsonResponse({
                'success': True,
                'message': ''
            })
        except Exception as ex:
            scraper = Scraper()
            if scraper.try_login(rut, clave):
                # create the user only if the external login was successful
                user_profile = create_user(
                    username=rut,
                    password=clave,
                    player_id=player_id)  # saves username, password, clave and player_id

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
