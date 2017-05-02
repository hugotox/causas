from django.contrib import admin

from main.models import *


class AdminCausa(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('user', 'id', 'rol', 'caratulado')
    search_fields = ('user__user__username', 'id', 'rol', 'caratulado')
    readonly_fields = ('created', 'modified')


class AdminDocSuprema(admin.ModelAdmin):
    search_fields = ('causa__rol', 'causa__caratulado', 'nomenclatura', 'descripcion')
    list_display = ('causa', 'nomenclatura', 'descripcion')
    readonly_fields = ('created', 'modified')


class AdminDocApelaciones(admin.ModelAdmin):
    search_fields = ('causa__rol', 'causa__caratulado', 'libro', 'nro_ingreso', 'descripcion')
    list_display = ('causa', 'libro', 'nro_ingreso', 'descripcion')
    readonly_fields = ('created', 'modified')


class AdminDocCivil(admin.ModelAdmin):
    search_fields = ('causa__rol', 'causa__caratulado', 'descripcion', 'tribunal')
    list_display = ('causa', 'descripcion', 'tribunal')
    readonly_fields = ('created', 'modified')


class AdminDocCivilEscrito(admin.ModelAdmin):
    search_fields = ('causa__rol', 'causa__caratulado', 'tipo', 'solicitante')
    list_display = ('causa', 'tipo', 'solicitante', 'fecha')
    readonly_fields = ('created', 'modified')


class AdminDocLaboral(admin.ModelAdmin):
    search_fields = ('causa__rol', 'causa__caratulado', 'tramite',)
    list_display = ('causa', 'tramite')
    readonly_fields = ('created', 'modified')


class AdminDocPenal(admin.ModelAdmin):
    search_fields = ('causa__rol', 'causa__caratulado', 'tribunal', 'observacion',)
    list_display = ('causa', 'tribunal', 'observacion')
    readonly_fields = ('created', 'modified')


class AdminDocCobranza(admin.ModelAdmin):
    search_fields = ('causa__rol', 'causa__caratulado', 'tramite', 'desc_tramite')
    list_display = ('causa', 'tramite', 'desc_tramite')
    readonly_fields = ('created', 'modified')


class AdminDocFamilia(admin.ModelAdmin):
    search_fields = ('causa__rol', 'causa__caratulado', 'tramite', 'desc_tramite')
    list_display = ('causa', 'tramite', 'desc_tramite')
    readonly_fields = ('created', 'modified')


class AdminNotification(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    search_fields = ('profile__user__username', 'heading', 'contents', 'document_type', 'document_id')
    list_display = ('profile', 'heading', 'contents', 'document_type', 'document_id')


class AdminComment(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('profile', 'contents', 'created', 'modified')


admin.site.register(UserProfile)
admin.site.register(Causa, AdminCausa)
admin.site.register(DocApelaciones, AdminDocApelaciones)
admin.site.register(DocSuprema, AdminDocSuprema)
admin.site.register(DocLaboral, AdminDocLaboral)
admin.site.register(DocPenal, AdminDocPenal)
admin.site.register(DocCivil, AdminDocCivil)
admin.site.register(EscritoCivilPorResolver, AdminDocCivilEscrito)
admin.site.register(DocCobranza, AdminDocCobranza)
admin.site.register(DocFamilia, AdminDocFamilia)
admin.site.register(Notification, AdminNotification)
admin.site.register(Comments, AdminComment)
