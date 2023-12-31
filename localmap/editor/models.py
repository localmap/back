from django.db import models
from django.conf import settings
from restaurant.models import Restaurant
import uuid
from urllib.parse import urlparse, unquote


class Editor(models.Model):
    ed_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_id = models.ManyToManyField(Restaurant, verbose_name="Restaurants")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user',
        to_field='name'
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    view = models.IntegerField(null=True, default=0)
    url = models.ImageField(null=True)

    class Meta:
        db_table = 'editor'
        verbose_name = 'Editor'
        verbose_name_plural = 'Editors'

    @property
    def file_url(self):
        parsed_url = urlparse(self.url.url)
        decoded_path = unquote(parsed_url.path)
        if decoded_path.startswith('/'):
            decoded_path = decoded_path[1:]
        return decoded_path
