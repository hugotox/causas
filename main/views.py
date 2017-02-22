import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from main.utils import external_login, create_user


def home(request):
    return HttpResponse('ok')


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        rut = data['rut']
        clave = data['clave']
        player_id = data['playerId']
        # TODO: use requests to validate the clave

        if external_login(rut, clave):
            user_profile = create_user(username=rut, password=clave,
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
