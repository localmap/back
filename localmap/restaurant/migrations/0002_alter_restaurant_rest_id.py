# Generated by Django 4.2.1 on 2023-06-23 22:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='rest_id',
            field=models.UUIDField(default=uuid.UUID('0a40a47b-2216-4bb4-bcbc-893c71442201'), editable=False, primary_key=True, serialize=False),
        ),
    ]