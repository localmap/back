# Generated by Django 4.2.1 on 2023-06-30 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0003_alter_restaurant_rest_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('Review_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contents', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rating', models.FloatField()),
                ('rest_id', models.ForeignKey(db_column='rest_id', on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
                ('user', models.ForeignKey(db_column='user', default='admin@admin.com', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email')),
            ],
            options={
                'db_table': 'review',
            },
        ),
    ]
