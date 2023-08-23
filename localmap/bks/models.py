from django.db import models
from django.conf import settings
from restaurant.models import Restaurant
import uuid

class Bk(models.Model):
    bk_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_id = models.ManyToManyField(Restaurant, verbose_name="Restaurants")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user',
        to_field='email',
        default='admin@admin.com',
        verbose_name="User"
    )

    class Meta:
        db_table = 'bk'
        verbose_name = 'Bk'
        verbose_name_plural = 'Bks'