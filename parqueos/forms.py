from django import forms
from .models import Parqueo

class ParqueoForm(forms.ModelForm):
    class Meta:
        model = Parqueo
        fields = ['direccion', 'id_estacion']
        labels = {
            'direccion': 'Dirección del parqueo (opcional)',
            'id_estacion': 'Estación asignada'
        }

    def clean_id_estacion(self):
        estacion = self.cleaned_data.get('id_estacion')
        if not estacion:
            raise forms.ValidationError("Debe seleccionar una estación.")
        return estacion
