# Generated by Django 4.2.1 on 2023-07-31 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0005_restaurant_location_alter_restaurant_latitude_and_more'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='category_name',
            field=models.ForeignKey(db_column='category_name', on_delete=django.db.models.deletion.CASCADE, to='restaurant.categories', to_field='category_name'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='name'),
        ),
    ]
