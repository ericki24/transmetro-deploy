from django import forms
from .models import Piloto

class PilotoForm(forms.ModelForm):
    class Meta:
        model = Piloto
        fields = ['nombre', 'direccion', 'telefono', 'escolaridad']
        labels = {
            'nombre': 'Nombre del piloto',
            'direccion': 'Dirección (opcional)',
            'telefono': 'Teléfono (opcional)',
            'escolaridad': 'Escolaridad (opcional)'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError("El nombre no puede estar vacío.")
        return nombre.title()
