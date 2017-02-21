from django.conf.urls import url
from main.views import *

urlpatterns = [
    url(r'^login/$', login),
    url(r'', home),
]
