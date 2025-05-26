from django.db import models

# Create your models here.
from django.db import models
from accesos.models import Acceso

class Guardia(models.Model):
    id_guardia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    id_acceso = models.ForeignKey(Acceso, models.DO_NOTHING, db_column='id_acceso')

    class Meta:
        managed = False
        db_table = 'guardia'

    def __str__(self):
            return self.nombre
    
class Meta:
    managed = False
    db_table = 'guardia'
    default_permissions = ()
    permissions = [
        ("view_guardia", "Puede ver guardias"),
        ("add_guardia", "Puede agregar guardias"),
        ("change_guardia", "Puede editar guardias"),
        ("delete_guardia", "Puede eliminar guardias"),
    ]
