# Generated by Django 4.2.1 on 2023-07-31 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0005_restaurant_location_alter_restaurant_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('ed_no', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('view', models.IntegerField(default=0, null=True)),
                ('rest_id', models.ManyToManyField(to='restaurant.restaurant', verbose_name='Restaurants')),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='name')),
            ],
            options={
                'verbose_name': 'Editor',
                'verbose_name_plural': 'Editors',
                'db_table': 'editor',
            },
        ),
    ]
