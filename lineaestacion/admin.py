from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import LineaEstacion

@admin.register(LineaEstacion)
class LineaEstacionAdmin(admin.ModelAdmin):
    list_display = ['id_linea_estacion', 'id_linea', 'id_estacion', 'orden', 'distancia_a_siguiente']
