from django.db import models
from django.conf import settings
from restaurant.models import Restaurant
import uuid

class Editor(models.Model):
    ed_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_id = models.ManyToManyField(Restaurant, verbose_name="Restaurants")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user',
        to_field='email',
        default='admin@admin.com',
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    content = models.TextField(verbose_name="Content")

    class Meta:
        db_table = 'editor'
        verbose_name = 'Editor'
        verbose_name_plural = 'Editors'