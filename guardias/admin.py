from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Guardia

@admin.register(Guardia)
class GuardiaAdmin(admin.ModelAdmin):
    list_display = ['id_guardia', 'nombre', 'id_acceso']
