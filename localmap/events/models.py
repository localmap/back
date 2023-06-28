from django.db import models
import uuid

class Events(models.Model):
    event_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_id = models.ForeignKey(
        'restaurant.Restaurant', on_delete=models.CASCADE, db_column='rest_id', to_field='rest_id', default='9e439580-d563-44fc-83d0-9da15ca2a872')
    name = models.CharField()
    amount = models.IntegerField()
    content = models.TextField(null=True)

    class Meta:
        db_table = 'events'