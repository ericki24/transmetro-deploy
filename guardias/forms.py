from django import forms
from .models import Guardia

class GuardiaForm(forms.ModelForm):
    class Meta:
        model = Guardia
        fields = ['nombre', 'id_acceso']
        labels = {
            'nombre': 'Nombre del guardia',
            'id_acceso': 'Acceso asignado'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError("El nombre no puede estar vacío.")
        return nombre.title()
