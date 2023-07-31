from django.db import models
import uuid

class Menu(models.Model):
    menu_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_id = models.ForeignKey(
        'restaurant.Restaurant', on_delete=models.CASCADE, db_column='rest_id', to_field='rest_id')
    name = models.CharField()
    price = models.IntegerField(null=True)

    class Meta:
        db_table = 'menu'