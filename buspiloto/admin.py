from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BusPiloto

@admin.register(BusPiloto)
class BusPilotoAdmin(admin.ModelAdmin):
    list_display = ['id_bus_piloto', 'id_bus', 'id_piloto']
