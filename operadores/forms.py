from django import forms
from .models import Operador

class OperadorForm(forms.ModelForm):
    class Meta:
        model = Operador
        fields = ['nombre', 'usuario', 'contrasena', 'id_estacion']
        labels = {
            'nombre': 'Nombre del operador (opcional)',
            'usuario': 'Usuario (opcional)',
            'contrasena': 'Contraseña (opcional)',
            'id_estacion': 'Estación asignada (única)'
        }

    def clean_id_estacion(self):
        estacion = self.cleaned_data.get('id_estacion')
        if not estacion:
            raise forms.ValidationError("Debe seleccionar una estación.")
        
        operadores = Operador.objects.all()
        if self.instance.pk:
            operadores = operadores.exclude(pk=self.instance.pk)
        if operadores.filter(id_estacion=estacion).exists():
            raise forms.ValidationError("Esta estación ya tiene un operador asignado.")
        
        return estacion
