from django.db import models
from hjd.models import Hjd
import uuid
from django.conf import settings


class Categories(models.Model):
    category_name = models.CharField(max_length=50,unique=True,)

    class Meta:
        db_table = 'categories'

class Restaurant(models.Model):
    rest_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    area_id = models.ForeignKey(Hjd, on_delete=models.CASCADE, db_column='area_id', to_field='id',default=1)
    category_name = models.ForeignKey(Categories, on_delete=models.CASCADE,db_column='category_name',to_field='category_name',default='한식')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='email',default='admin@admin.com')
    name = models.CharField()
    address = models.CharField(null=True)
    view = models.IntegerField(null=True, default=0)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 생성시 자동으로 시간저장
    updated_at = models.DateTimeField(auto_now=True) # 수정시 자동으로 시간저장
    latitude = models.FloatField()
    longitude = models.FloatField()
    introduce = models.TextField(null=True)

    class Meta:
        db_table = 'restaurant'
