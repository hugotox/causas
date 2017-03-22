# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userprofile_player_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='docapelaciones',
            options={'verbose_name_plural': 'Docs. Apelaciones'},
        ),
        migrations.AlterModelOptions(
            name='doccivil',
            options={'verbose_name_plural': 'Docs. Civil'},
        ),
        migrations.AlterModelOptions(
            name='doccobranza',
            options={'verbose_name_plural': 'Docs. Cobranza'},
        ),
        migrations.AlterModelOptions(
            name='docfamilia',
            options={'verbose_name_plural': 'Docs. Familia'},
        ),
        migrations.AlterModelOptions(
            name='doclaboral',
            options={'verbose_name_plural': 'Docs. Laboral'},
        ),
        migrations.AlterModelOptions(
            name='docpenal',
            options={'verbose_name_plural': 'Docs. Penal'},
        ),
        migrations.AlterModelOptions(
            name='docsuprema',
            options={'verbose_name_plural': 'Docs. Suprema'},
        ),
        migrations.AlterField(
            model_name='doclaboral',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]