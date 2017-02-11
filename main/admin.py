from django.contrib import admin

# Register your models here.
from main.models import UserProfile, Causa

admin.site.register(UserProfile)
admin.site.register(Causa)
