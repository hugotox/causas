# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 22:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Causa',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'Corte Suprema'), (2, 'Corte Apelaciones'), (3, 'Civil'), (4, 'Laboral'), (5, 'Penal'), (6, 'Cobranza'), (7, 'Familia')])),
                ('archived', models.BooleanField(default=False)),
                ('caratulado', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('clave', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='causa',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserProfile'),
        ),
    ]
