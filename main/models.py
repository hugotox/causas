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
    caratulado = models.CharField(max_length=200)

    def __str__(self):
        return '{} - {} (Archived: {})'.format(self.id, self.caratulado, self.archived)


class Document(models.Model):
    """
    Suprema
    - Folio (num)
    - Doc (icon)
    - Año Folio (num)
    - Fecha Resolucion (date)
    - Tipo Tramite (text)
    - Nomenclatura (text)
    - Des. Trámite (text)
    - Salas (text)

    Apelaciones
    - Doc. (icon)
    - Tipo Tramite (text)
    - Folio (num)
    - Descripcion (text)
    - Fecha (date)
    - Sala (text)
    - Foja Inicial (num)

    Civil
    - Folio (num)
    - Doc (icon)
    - Anexo (icon)
    - Etapa (text)
    - Trámite (text)
    - Desc. Trámite (text)
    - Fec. Trámite (date)
    - Foja (num)

    Laboral
    - Doc. (icon)
    - Anexo (icon)
    - Tipo Tramite (text)
    - Tramite (text)
    - Fecha (date)

    Penal
    - Doc (icon)
    - Tipo
    - Observación (text)
    - Fecha (date)
    - Estado (text)
    - Estado Cambio Estado (date)

    Cobranza
    - Doc. Sel. (icon)
    - Etapa (text)
    - Trámite (text)
    - Desc. Trámite (text)
    - Fech. Tram. (date)

    Familia
    - Doc. (icon)
    - Anexo (icon)
    - Etapa (text)
    - Trámite (text)
    - Desc. Trámite (text)
    - Referencia (text)
    - Fecha Tram. (date)
    """

    # TODO: how to identify a document
    causa = models.ForeignKey(Causa)
