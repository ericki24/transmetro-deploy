from django.db import models

# Create your models here.
from django.db import models
from municipios.models import Municipalidad

class Estacion(models.Model):
    id_estacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    capacidad = models.IntegerField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    id_municipalidad = models.ForeignKey(Municipalidad, models.DO_NOTHING, db_column='id_municipalidad')

    class Meta:
        managed = False
        db_table = 'estacion'

    def __str__(self):
        return self.nombre


class Meta:
    managed = False
    db_table = 'estacion'
    default_permissions = ()
    permissions = [
        ("view_estacion", "Puede ver estaciones"),
        ("add_estacion", "Puede agregar estaciones"),
        ("change_estacion", "Puede editar estaciones"),
        ("delete_estacion", "Puede eliminar estaciones"),
    ]