from django.db import models
from restaurant.models import Restaurant
from django.conf import settings
import uuid
from urllib.parse import urlparse, unquote

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, db_column='rest_id', related_name='rest_rev')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='name')
    title = models.CharField(max_length=100)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 생성시 자동으로 시간저장
    rating = models.FloatField()
    is_verified = models.BooleanField(default=False)


    class Meta:
        db_table = 'review'

class Photos(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(Review, related_name='photos', on_delete=models.CASCADE,default=1)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='name')
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.ImageField()

    class Meta:
        db_table = 'photos'

    @property
    def file_url(self):
        parsed_url = urlparse(self.url.url)
        decoded_path = unquote(parsed_url.path)
        if decoded_path.startswith('/'):
            decoded_path = decoded_path[1:]
        return decoded_path
