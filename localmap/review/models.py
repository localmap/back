from django.db import models
from restaurant.models import Restaurant
from django.conf import settings
import uuid

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, db_column='rest_id', related_name='rest_rev')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='email',
        default='admin@admin.com')
    title = models.CharField(max_length=100, default='맛있어요')
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 생성시 자동으로 시간저장
    rating = models.FloatField()
    is_verified = models.BooleanField(default=False)


    class Meta:
        db_table = 'review'

class Photos(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(Review, related_name='photos', on_delete=models.CASCADE,default=1)
    email = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='email',
        default='admin@admin.com')
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.ImageField()

    class Meta:
        db_table = 'photos'

    @property
    def file_url(self):
        return self.url.url
