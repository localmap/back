# Generated by Django 4.2.1 on 2023-08-06 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='editor',
            name='url',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]