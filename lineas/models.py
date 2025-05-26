from django.db import models

# Create your models here.
from django.db import models
from municipios.models import Municipalidad

class Linea(models.Model):
    id_linea = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    color = models.CharField(max_length=10, blank=True, null=True)
    distancia_total = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    id_municipalidad = models.ForeignKey(Municipalidad, models.DO_NOTHING, db_column='id_municipalidad')

    class Meta:
        managed = False
        db_table = 'linea'


    def __str__(self):
            return self.nombre
    
class Meta:
    managed = False
    db_table = 'linea'
    default_permissions = ()
    permissions = [
        ("view_linea", "Puede ver líneas"),
        ("add_linea", "Puede agregar líneas"),
        ("change_linea", "Puede editar líneas"),
        ("delete_linea", "Puede eliminar líneas"),
    ]