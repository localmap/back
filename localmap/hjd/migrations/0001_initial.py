# Generated by Django 4.2.1 on 2023-06-21 20:52

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hjd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('adm_nm', models.CharField()),
                ('sidonm', models.CharField()),
                ('temp', models.CharField()),
                ('sggnm', models.CharField()),
            ],
            options={
                'db_table': 'hjd',
            },
        ),
    ]
