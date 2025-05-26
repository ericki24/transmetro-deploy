from django import forms
from .models import Linea
import re
import unicodedata

class LineaForm(forms.ModelForm):
    class Meta:
        model = Linea
        fields = ['nombre', 'color', 'distancia_total', 'id_municipalidad']
        labels = {
            'nombre': 'Nombre de la línea',
            'color': 'Color (ej: #0d6efd)',
            'distancia_total': 'Distancia total (km)',
            'id_municipalidad': 'Municipalidad a la que pertenece'
        }
        widgets = {
            'color': forms.TextInput(attrs={'placeholder': '#0d6efd'}),
            'distancia_total': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def normalizar(self, texto):
        texto = unicodedata.normalize('NFD', texto)
        texto = texto.encode('ascii', 'ignore').decode('utf-8')
        texto = re.sub(r'\s+', '', texto)
        return texto.lower()

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre_normalizado = self.normalizar(nombre)

        lineas = Linea.objects.all()
        if self.instance.pk:
            lineas = lineas.exclude(pk=self.instance.pk)

        for l in lineas:
            if self.normalizar(l.nombre) == nombre_normalizado:
                raise forms.ValidationError("Este nombre de línea ya está registrado (sin importar espacios o mayúsculas).")

        return nombre.strip().title()
