from django.db import models

# Create your models here.
from django.db import models
from lineas.models import Linea
from parqueos.models import Parqueo

class Bus(models.Model):
    id_bus = models.AutoField(primary_key=True)
    placa = models.CharField(unique=True, max_length=20)
    capacidad = models.IntegerField(blank=True, null=True)
    id_linea = models.ForeignKey(Linea, models.DO_NOTHING, db_column='id_linea', blank=True, null=True)
    id_parqueo = models.ForeignKey(Parqueo, models.DO_NOTHING, db_column='id_parqueo')

    class Meta:
        managed = False
        db_table = 'bus'
        
    def __str__(self):
            return self.placa
    

class Meta:
    managed = False
    db_table = 'bus'
    default_permissions = ()
    permissions = [
        ("view_bus", "Puede ver buses"),
        ("add_bus", "Puede agregar buses"),
        ("change_bus", "Puede editar buses"),
        ("delete_bus", "Puede eliminar buses"),
    ]
