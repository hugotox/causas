from django.contrib import admin

from main.models import UserProfile, Causa, DocFamilia, DocCobranza, DocCivil, DocPenal, DocLaboral, DocApelaciones, \
    DocSuprema


class AdminCausa(admin.ModelAdmin):
    list_filter = ('type',)

    class Meta:
        model = Causa


class AdminDocLaboral(admin.ModelAdmin):
    search_fields = ('tramite',)


admin.site.register(UserProfile)
admin.site.register(Causa, AdminCausa)
admin.site.register(DocApelaciones)
admin.site.register(DocSuprema)
admin.site.register(DocLaboral, AdminDocLaboral)
admin.site.register(DocPenal)
admin.site.register(DocCivil)
admin.site.register(DocCobranza)
admin.site.register(DocFamilia)
