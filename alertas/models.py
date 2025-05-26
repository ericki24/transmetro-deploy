from django.db import models

# Create your models here.
from django.db import models
from estaciones.models import Estacion

class Alerta(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(blank=True, null=True)
    id_estacion = models.ForeignKey(Estacion, models.DO_NOTHING, db_column='id_estacion')

    class Meta:
        managed = False
        db_table = 'alerta'

    def __str__(self):
            return f"Alerta: {self.mensaje}"
    



class Meta:
    managed = False
    db_table = 'alerta'
    default_permissions = ()
    permissions = [
        ("view_alerta", "Puede ver alertas"),
        ("add_alerta", "Puede agregar alertas"),
        ("change_alerta", "Puede editar alertas"),
        ("delete_alerta", "Puede eliminar alertas"),
    ]
