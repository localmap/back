from django.contrib.gis.db import models

class Hjd(models.Model):
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    adm_nm = models.CharField(blank=True, null=True)
    sidonm = models.CharField(blank=True, null=True)
    temp = models.CharField(blank=True, null=True)
    sggnm = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hjd'
