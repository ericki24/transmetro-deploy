from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Parqueo

@admin.register(Parqueo)
class ParqueoAdmin(admin.ModelAdmin):
    list_display = ['id_parqueo', 'direccion', 'id_estacion']
