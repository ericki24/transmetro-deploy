from django.db import models

# Create your models here.
from django.db import models
from lineas.models import Linea
from estaciones.models import Estacion

class LineaEstacion(models.Model):
    id_linea_estacion = models.AutoField(primary_key=True)
    id_linea = models.ForeignKey(Linea, models.DO_NOTHING, db_column='id_linea')
    id_estacion = models.ForeignKey(Estacion, models.DO_NOTHING, db_column='id_estacion')
    orden = models.IntegerField()
    distancia_a_siguiente = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linea_estacion'

    def __str__(self):
            return f"{self.id_linea.nombre} - {self.id_estacion.nombre} (Orden {self.orden})"
    
class Meta:
    managed = False
    db_table = 'linea_estacion'
    default_permissions = ()
    permissions = [
        ("view_lineaestacion", "Puede ver asignación línea-estación"),
        ("add_lineaestacion", "Puede agregar asignación línea-estación"),
        ("change_lineaestacion", "Puede editar asignación línea-estación"),
        ("delete_lineaestacion", "Puede eliminar asignación línea-estación"),
    ]