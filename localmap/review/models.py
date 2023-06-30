from django.db import models
from restaurant.models import Restaurant
from django.conf import settings
import uuid

class Review(models.Model):
    Review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, db_column='rest_id')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='email',
        default='admin@admin.com')
    title = models.CharField(max_length=100, default='맛있어요')
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 생성시 자동으로 시간저장
    rating = models.FloatField()

    class Meta:
        db_table = 'review'

