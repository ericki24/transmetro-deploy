from django.db import models

# Create your models here.
from django.db import models

class Piloto(models.Model):
    id_piloto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    escolaridad = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'piloto'


    def __str__(self):
            return self.nombre
    
class Meta:
    managed = False
    db_table = 'piloto'
    default_permissions = ()
    permissions = [
        ("view_piloto", "Puede ver pilotos"),
        ("add_piloto", "Puede agregar pilotos"),
        ("change_piloto", "Puede editar pilotos"),
        ("delete_piloto", "Puede eliminar pilotos"),
    ]
