from django.db import models

# Create your models here.
from django.db import models
from estaciones.models import Estacion

class Acceso(models.Model):
    id_acceso = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    id_estacion = models.ForeignKey(Estacion, models.DO_NOTHING, db_column='id_estacion')

    class Meta:
        managed = False
        db_table = 'acceso'

    
    def __str__(self):
        return self.descripcion or f"Acceso #{self.id_acceso}"


class Meta:
    managed = False
    db_table = 'acceso'
    default_permissions = ()
    permissions = [
        ("view_acceso", "Puede ver accesos"),
        ("add_acceso", "Puede agregar accesos"),
        ("change_acceso", "Puede editar accesos"),
        ("delete_acceso", "Puede eliminar accesos"),
    ]