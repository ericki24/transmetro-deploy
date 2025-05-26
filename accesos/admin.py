from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Acceso

@admin.register(Acceso)
class AccesoAdmin(admin.ModelAdmin):
    list_display = ['id_acceso', 'descripcion', 'id_estacion']
