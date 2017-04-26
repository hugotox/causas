from django.conf.urls import url
from django.views.generic import RedirectView

from main.views import *

urlpatterns = [
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^api/notifications/$', notifications),
    url(r'', RedirectView.as_view(url='/admin/')),
]
