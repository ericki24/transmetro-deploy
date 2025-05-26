from django import forms
from .models import Acceso

class AccesoForm(forms.ModelForm):
    class Meta:
        model = Acceso
        fields = ['descripcion', 'id_estacion']
        labels = {
            'descripcion': 'Descripción del acceso (opcional)',
            'id_estacion': 'Estación a la que pertenece'
        }

    def clean_id_estacion(self):
        estacion = self.cleaned_data.get('id_estacion')
        if not estacion:
            raise forms.ValidationError("Debe seleccionar una estación.")
        return estacion
