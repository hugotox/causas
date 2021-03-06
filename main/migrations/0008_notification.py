# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 22:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20170327_2332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.TextField()),
                ('contents', models.TextField()),
                ('player_id', models.TextField()),
                ('document_type', models.IntegerField()),
                ('document_id', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserProfile')),
            ],
            options={
                'verbose_name_plural': 'Notificaciones',
            },
        ),
    ]
