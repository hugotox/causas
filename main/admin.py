from django.contrib import admin

from main.models import UserProfile, Causa, DocFamilia, DocCobranza, DocCivil, DocPenal, DocLaboral, DocApelaciones, \
    DocSuprema

admin.site.register(UserProfile)
admin.site.register(Causa)
admin.site.register(DocApelaciones)
admin.site.register(DocSuprema)
admin.site.register(DocLaboral)
admin.site.register(DocPenal)
admin.site.register(DocCivil)
admin.site.register(DocCobranza)
admin.site.register(DocFamilia)
