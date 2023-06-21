# Generated by Django 4.2.1 on 2023-06-21 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hjd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('rest_id', models.UUIDField(default=uuid.UUID('076bc7a3-13bf-4fdb-ae6d-471861c6d908'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField()),
                ('view', models.IntegerField(default=0, null=True)),
                ('contents', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('introduce', models.TextField(null=True)),
                ('area_id', models.ForeignKey(db_column='area_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='hjd.hjd')),
                ('category_name', models.ForeignKey(db_column='category_name', default='한식', on_delete=django.db.models.deletion.CASCADE, to='restaurant.categories', to_field='category_name')),
                ('user', models.ForeignKey(db_column='user', default='admin@admin.com', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email')),
            ],
            options={
                'db_table': 'restaurant',
            },
        ),
    ]