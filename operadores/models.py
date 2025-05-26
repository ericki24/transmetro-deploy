from django.db import models

# Create your models here.
from django.db import models
from estaciones.models import Estacion

class Operador(models.Model):
    id_operador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    contrasena = models.CharField(max_length=100, blank=True, null=True)
    id_estacion = models.OneToOneField(Estacion, models.DO_NOTHING, db_column='id_estacion')

    class Meta:
        managed = False
        db_table = 'operador'


    def __str__(self):
            return self.nombre
    
class Meta:
    managed = False
    db_table = 'operador'
    default_permissions = ()
    permissions = [
        ("view_operador", "Puede ver operadores"),
        ("add_operador", "Puede agregar operadores"),
        ("change_operador", "Puede editar operadores"),
        ("delete_operador", "Puede eliminar operadores"),
    ]