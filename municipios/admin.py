from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Municipalidad

@admin.register(Municipalidad)
class MunicipalidadAdmin(admin.ModelAdmin):
    list_display = ['id_municipalidad', 'nombre']
