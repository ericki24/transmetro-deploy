from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Estacion

@admin.register(Estacion)
class EstacionAdmin(admin.ModelAdmin):
    list_display = ['id_estacion', 'nombre', 'ubicacion', 'capacidad', 'latitud', 'longitud', 'id_municipalidad']
