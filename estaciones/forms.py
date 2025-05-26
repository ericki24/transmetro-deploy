from django import forms
from .models import Estacion
import re
import unicodedata

class EstacionForm(forms.ModelForm):
    class Meta:
        model = Estacion
        fields = ['nombre', 'ubicacion', 'capacidad', 'latitud', 'longitud', 'id_municipalidad']
        labels = {
            'nombre': 'Nombre de la estación',
            'ubicacion': 'Ubicación (opcional)',
            'capacidad': 'Capacidad máxima',
            'latitud': 'Latitud (opcional)',
            'longitud': 'Longitud (opcional)',
            'id_municipalidad': 'Municipalidad a la que pertenece'
        }
        widgets = {
            'capacidad': forms.NumberInput(attrs={'min': 1}),
            'latitud': forms.NumberInput(attrs={'step': '0.0000001'}),
            'longitud': forms.NumberInput(attrs={'step': '0.0000001'}),
        }

    def normalizar(self, texto):
        texto = unicodedata.normalize('NFD', texto)
        texto = texto.encode('ascii', 'ignore').decode('utf-8')
        texto = re.sub(r'\s+', '', texto)
        return texto.lower()

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre_normalizado = self.normalizar(nombre)

        estaciones = Estacion.objects.all()
        if self.instance.pk:
            estaciones = estaciones.exclude(pk=self.instance.pk)

        for e in estaciones:
            if self.normalizar(e.nombre) == nombre_normalizado:
                raise forms.ValidationError("Este nombre ya está registrado (sin importar espacios o mayúsculas).")

        return nombre.strip().title()
