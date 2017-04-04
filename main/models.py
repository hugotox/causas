from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20, null=True, blank=True)
    initial_migration_done = models.BooleanField(default=False)
    clave = models.TextField()
    player_id = models.TextField(blank=True, null=True)  # serialized array of player_ids

    def __str__(self):
        return '{}'.format(self.user.username)


class Causa(models.Model):
    TYPE_CHOICES_SUPREMA = 1
    TYPE_CHOICES_APELACIONES = 2
    TYPE_CHOICES_CIVIL = 3
    TYPE_CHOICES_LABORAL = 4
    TYPE_CHOICES_PENAL = 5
    TYPE_CHOICES_COBRANZA = 6
    TYPE_CHOICES_FAMILIA = 7

    TYPE_CHOICES = (
        (TYPE_CHOICES_SUPREMA, 'Corte Suprema'),
        (TYPE_CHOICES_APELACIONES, 'Corte Apelaciones'),
        (TYPE_CHOICES_CIVIL, 'Civil'),
        (TYPE_CHOICES_LABORAL, 'Laboral'),
        (TYPE_CHOICES_PENAL, 'Penal'),
        (TYPE_CHOICES_COBRANZA, 'Cobranza'),
        (TYPE_CHOICES_FAMILIA, 'Familia'),
    )
    id = models.TextField(primary_key=True)
    rol = models.TextField(default='')
    user = models.ForeignKey(UserProfile)
    type = models.IntegerField(choices=TYPE_CHOICES)
    archived = models.BooleanField(default=False)
    caratulado = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.rol, self.caratulado)


class DocSuprema(models.Model):
    id = models.TextField(primary_key=True)  # id format is "<causa.id>__<iddoc>"
    causa = models.ForeignKey(Causa)
    anio = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)
    nomenclatura = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    salas = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Docs. Suprema'

    def __str__(self):
        return '{}'.format(self.nomenclatura)


class DocApelaciones(models.Model):
    id = models.TextField(primary_key=True)  # id format is "<causa.id>__<folio>"
    causa = models.ForeignKey(Causa)
    tipo = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    salas = models.TextField(blank=True, null=True)
    foja_inicial = models.TextField(blank=True, null=True)
    libro = models.TextField(blank=True, null=True)
    nro_ingreso = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Docs. Apelaciones'

    def __str__(self):
        return '{} - {} - {}'.format(self.libro, self.nro_ingreso, self.descripcion)


class DocCivil(models.Model):
    id = models.TextField(primary_key=True)  # id format is "<causa.id>__<folio>"
    causa = models.ForeignKey(Causa)
    etapa = models.TextField(blank=True, null=True)
    tramite = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    tribunal = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    foja = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Docs. Civil'

    def __str__(self):
        return '{} - {}'.format(self.descripcion, self.tribunal)


class DocLaboral(models.Model):
    id = models.TextField(primary_key=True)
    causa = models.ForeignKey(Causa)
    tipo = models.TextField(blank=True, null=True)
    tramite = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Docs. Laboral'

    def __str__(self):
        return '{}'.format(self.tramite)


class DocPenal(models.Model):
    id = models.TextField(primary_key=True)
    causa = models.ForeignKey(Causa)
    tipo = models.TextField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    tribunal = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    cambio_estado = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Docs. Penal'

    def __str__(self):
        return '{} - {}'.format(self.tribunal, self.observacion)


class DocCobranza(models.Model):
    id = models.TextField(primary_key=True)
    causa = models.ForeignKey(Causa)
    etapa = models.TextField(blank=True, null=True)
    tramite = models.TextField(blank=True, null=True)
    desc_tramite = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Docs. Cobranza'

    def __str__(self):
        return '{}'.format(self.desc_tramite)


class DocFamilia(models.Model):
    id = models.TextField(primary_key=True)
    causa = models.ForeignKey(Causa)
    etapa = models.TextField(blank=True, null=True)
    tramite = models.TextField(blank=True, null=True)
    desc_tramite = models.TextField(blank=True, null=True)
    referencia = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Docs. Familia'

    def __str__(self):
        return '{}'.format(self.desc_tramite)


class Notification(models.Model):
    profile = models.ForeignKey(UserProfile)
    heading = models.TextField()
    contents = models.TextField()
    player_id = models.TextField()
    document_type = models.IntegerField()
    document_id = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created']

    def __str__(self):
        return '{}: {}'.format(self.profile, self.heading)
