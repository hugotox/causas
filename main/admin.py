from django.contrib import admin

from main.models import UserProfile, Causa, DocFamilia, DocCobranza, DocCivil, DocPenal, DocLaboral, DocApelaciones, \
    DocSuprema


class AdminDocSuprema(admin.ModelAdmin):
    search_fields = ('id', 'nomenclatura', 'descripcion')


class AdminDocApelaciones(admin.ModelAdmin):
    search_fields = ('id', 'descripcion')


class AdminDocCivil(admin.ModelAdmin):
    search_fields = ('id', 'tramite', 'descripcion')


class AdminDocLaboral(admin.ModelAdmin):
    search_fields = ('id', 'tramite',)


class AdminDocPenal(admin.ModelAdmin):
    search_fields = ('id', 'observacion',)


class AdminDocCobranza(admin.ModelAdmin):
    search_fields = ('id', 'tramite',)


class AdminDocFamilia(admin.ModelAdmin):
    search_fields = ('id', 'tramite',)


class AdminCausa(admin.ModelAdmin):
    list_filter = ('type',)
    search_fields = ('id', 'caratulado')


admin.site.register(UserProfile)
admin.site.register(Causa, AdminCausa)
admin.site.register(DocApelaciones, AdminDocApelaciones)
admin.site.register(DocSuprema, AdminDocSuprema)
admin.site.register(DocLaboral, AdminDocLaboral)
admin.site.register(DocPenal, AdminDocPenal)
admin.site.register(DocCivil, AdminDocCivil)
admin.site.register(DocCobranza, AdminDocCobranza)
admin.site.register(DocFamilia, AdminDocFamilia)
