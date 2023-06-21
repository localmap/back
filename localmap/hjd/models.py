from django.contrib.gis.db import models

class Hjd(models.Model):
    geom = models.GeometryField()
    adm_nm = models.CharField()
    sidonm = models.CharField()
    temp = models.CharField()
    sggnm = models.CharField()

    class Meta:
        db_table = 'hjd'
