from django.db import models

# Create your models here.
from django.db import models
from estaciones.models import Estacion

class Parqueo(models.Model):
    id_parqueo = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    id_estacion = models.ForeignKey(Estacion, models.DO_NOTHING, db_column='id_estacion')

    class Meta:
        managed = False
        db_table = 'parqueo'


    def __str__(self):
            return self.direccion

class Meta:
    managed = False
    db_table = 'parqueo'
    default_permissions = ()
    permissions = [
        ("view_parqueo", "Puede ver parqueos"),
        ("add_parqueo", "Puede agregar parqueos"),
        ("change_parqueo", "Puede editar parqueos"),
        ("delete_parqueo", "Puede eliminar parqueos"),
    ]