from django.conf.urls import url
from django.views.generic import RedirectView

from main.views import *

urlpatterns = [
    url(r'^login/$', login),
    url(r'^api/notifications/(?P<rut>\w+)', notifications),
    url(r'', RedirectView.as_view(url='/admin/')),
]
