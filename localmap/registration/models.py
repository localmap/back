from django.db import models
import uuid
from django.conf import settings

class Registration(models.Model):
    regist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.ForeignKey('restaurant.Categories', on_delete=models.CASCADE,db_column='category_name',to_field='category_name',default='한식')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='email',default='admin@admin.com')
    name = models.CharField()
    address = models.CharField(null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'registration'
