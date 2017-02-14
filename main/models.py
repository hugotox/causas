from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20, null=True, blank=True)
    initial_migration_done = models.BooleanField(default=False)
    clave = models.TextField()

    def __str__(self):
        return '{} {} ({})'.format(self.user.first_name, self.user.last_name, self.user.username)


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
    id = models.CharField(max_length=50, primary_key=True)  # uses Causa's "ROL" or "RIT" field
    user = models.ForeignKey(UserProfile)
    type = models.IntegerField(choices=TYPE_CHOICES)
    archived = models.BooleanField(default=False)
    caratulado = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} - {} (Archived: {})'.format(self.id, self.caratulado, self.archived)


class DocSuprema(models.Model):
    id = models.CharField(max_length=100, primary_key=True)  # id format is "<causa.id>-<folio>"
    causa = models.ForeignKey(Causa)
    anio = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)
    nomenclatura = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    salas = models.TextField(blank=True, null=True)


class DocApelaciones(models.Model):
    id = models.CharField(max_length=100, primary_key=True)  # id format is "<causa.id>-<folio>"
    causa = models.ForeignKey(Causa)
    tipo = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    salas = models.TextField(blank=True, null=True)
    foja_inicial = models.TextField(blank=True, null=True)


class DocCivil(models.Model):
    id = models.CharField(max_length=100, primary_key=True)  # id format is "<causa.id>-<folio>"
    causa = models.ForeignKey(Causa)
    etapa = models.TextField(blank=True, null=True)
    tramite = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    foja = models.TextField(blank=True, null=True)


class DocLaboral(models.Model):
    # uses auto generated id
    causa = models.ForeignKey(Causa)
    tipo = models.TextField(blank=True, null=True)
    tramite = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)


class DocPenal(models.Model):
    # uses auto generated id
    causa = models.ForeignKey(Causa)
    tipo = models.TextField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    cambio_estado = models.TextField(blank=True, null=True)


class DocCobranza(models.Model):
    # uses auto generated id
    causa = models.ForeignKey(Causa)
    etapa = models.TextField(blank=True, null=True)
    tramite = models.TextField(blank=True, null=True)
    desc_tramite = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)


class DocFamilia(models.Model):
    # uses auto generated id
    causa = models.ForeignKey(Causa)
    etapa = models.TextField(blank=True, null=True)
    tramite = models.TextField(blank=True, null=True)
    desc_tramite = models.TextField(blank=True, null=True)
    referencia = models.TextField(blank=True, null=True)
    fecha = models.TextField(blank=True, null=True)
