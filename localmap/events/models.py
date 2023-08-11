from django.db import models
import uuid

class Events(models.Model):
    event_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_id = models.ForeignKey(
        'restaurant.Restaurant', on_delete=models.CASCADE, db_column='rest_id', to_field='rest_id')
    name = models.CharField()
    amount = models.IntegerField()
    content = models.TextField(null=True)
    url = models.ImageField(null=True)

    class Meta:
        db_table = 'events'

    @property
    def file_url(self):
        return self.url.url