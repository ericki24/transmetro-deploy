from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Linea

@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ['id_linea', 'nombre', 'color', 'distancia_total', 'id_municipalidad']
