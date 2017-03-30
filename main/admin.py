from django.contrib import admin

from main.models import *


class AdminDocSuprema(admin.ModelAdmin):
    search_fields = ('id', 'nomenclatura', 'descripcion')
    readonly_fields = ('created', 'modified')


class AdminDocApelaciones(admin.ModelAdmin):
    search_fields = ('id', 'descripcion')
    readonly_fields = ('created', 'modified')


class AdminDocCivil(admin.ModelAdmin):
    search_fields = ('id', 'tramite', 'descripcion')
    readonly_fields = ('created', 'modified')


class AdminDocLaboral(admin.ModelAdmin):
    search_fields = ('id', 'tramite',)
    readonly_fields = ('created', 'modified')


class AdminDocPenal(admin.ModelAdmin):
    search_fields = ('id', 'observacion',)
    readonly_fields = ('created', 'modified')


class AdminDocCobranza(admin.ModelAdmin):
    search_fields = ('id', 'tramite',)
    readonly_fields = ('created', 'modified')


class AdminDocFamilia(admin.ModelAdmin):
    search_fields = ('id', 'tramite',)
    readonly_fields = ('created', 'modified')


class AdminCausa(admin.ModelAdmin):
    list_filter = ('type',)
    search_fields = ('id', 'caratulado')
    readonly_fields = ('created', 'modified')


admin.site.register(UserProfile)
admin.site.register(Causa, AdminCausa)
admin.site.register(DocApelaciones, AdminDocApelaciones)
admin.site.register(DocSuprema, AdminDocSuprema)
admin.site.register(DocLaboral, AdminDocLaboral)
admin.site.register(DocPenal, AdminDocPenal)
admin.site.register(DocCivil, AdminDocCivil)
admin.site.register(DocCobranza, AdminDocCobranza)
admin.site.register(DocFamilia, AdminDocFamilia)
admin.site.register(Notification)
