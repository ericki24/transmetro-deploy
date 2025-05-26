from django.db import models

# Create your models here.
from django.db import models

class Municipalidad(models.Model):
    id_municipalidad = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'municipalidad'

    def __str__(self):
            return self.nombre


# 9. municipalidad
class Meta:
    managed = False
    db_table = 'municipalidad'
    default_permissions = ()
    permissions = [
        ("view_municipalidad", "Puede ver municipalidades"),
        ("add_municipalidad", "Puede agregar municipalidades"),
        ("change_municipalidad", "Puede editar municipalidades"),
        ("delete_municipalidad", "Puede eliminar municipalidades"),
    ]