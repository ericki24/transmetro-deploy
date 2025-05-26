from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Operador

@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ['id_operador', 'nombre', 'usuario', 'contrasena', 'id_estacion']
