from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Alerta

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['id_alerta', 'mensaje', 'fecha', 'id_estacion']
