from django.contrib.gis.db import models
from hjd.models import Hjd
import uuid
from django.conf import settings
from django.contrib.gis.geos import Point


class Categories(models.Model):
    category_name = models.CharField(max_length=50,unique=True,)

    class Meta:
        db_table = 'categories'

class Restaurant(models.Model):
    rest_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    area_id = models.ForeignKey(Hjd, on_delete=models.CASCADE, db_column='area_id', to_field='id',default=1)
    category_name = models.ForeignKey(Categories, on_delete=models.CASCADE,db_column='category_name',to_field='category_name',default='한식')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='name')
    name = models.CharField()
    address = models.CharField(null=True)
    view = models.IntegerField(null=True, default=0)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 생성시 자동으로 시간저장
    updated_at = models.DateTimeField(auto_now=True) # 수정시 자동으로 시간저장
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    location = models.PointField(null=True)
    introduce = models.TextField(null=True)

    def save(self, *args, **kwargs):
        # 위도와 경도를 사용하여 Point 객체 생성
        self.location = Point(self.longitude, self.latitude)

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'restaurant'
