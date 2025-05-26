from django.db import models

# Create your models here.
from django.db import models
from buses.models import Bus
from pilotos.models import Piloto

class BusPiloto(models.Model):
    id_bus_piloto = models.AutoField(primary_key=True)
    id_bus = models.ForeignKey(Bus, models.DO_NOTHING, db_column='id_bus')
    id_piloto = models.ForeignKey(Piloto, models.DO_NOTHING, db_column='id_piloto')

    class Meta:
        managed = False
        db_table = 'bus_piloto'

    def __str__(self):
            return self.nombre
    
class Meta:
    managed = False
    db_table = 'bus_piloto'
    default_permissions = ()
    permissions = [
        ("view_buspiloto", "Puede ver asignación bus-piloto"),
        ("add_buspiloto", "Puede agregar asignación bus-piloto"),
        ("change_buspiloto", "Puede editar asignación bus-piloto"),
        ("delete_buspiloto", "Puede eliminar asignación bus-piloto"),
    ]