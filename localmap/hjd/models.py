from django.contrib.gis.db import models

class Hjd(models.Model):
    geom = models.GeometryField()
    adm_nm = models.CharField(unique=True)
    sidonm = models.CharField()
    temp = models.CharField()
    sggnm = models.CharField()
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)


    class Meta:
        db_table = 'hjd'

