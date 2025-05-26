from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Piloto

@admin.register(Piloto)
class PilotoAdmin(admin.ModelAdmin):
    list_display = ['id_piloto', 'nombre', 'direccion', 'telefono', 'escolaridad']
