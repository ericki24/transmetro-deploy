from django import forms
from .models import Municipalidad
import re
import unicodedata

class MunicipalidadForm(forms.ModelForm):
    class Meta:
        model = Municipalidad
        fields = ['nombre']
        labels = {'nombre': 'Nombre de la municipalidad'}

    def normalizar(self, texto):
        # Quitar acentos, convertir a minúsculas, quitar espacios internos
        texto = unicodedata.normalize('NFD', texto)
        texto = texto.encode('ascii', 'ignore').decode('utf-8')
        texto = re.sub(r'\s+', '', texto)  # Quitar todos los espacios
        return texto.lower()

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre_normalizado = self.normalizar(nombre)

        municipios = Municipalidad.objects.all()
        if self.instance.pk:
            municipios = municipios.exclude(pk=self.instance.pk)

        for m in municipios:
            if self.normalizar(m.nombre) == nombre_normalizado:
                raise forms.ValidationError("Este nombre ya está registrado, incluso si parece diferente por espacios o mayúsculas.")
        
        return nombre.strip().title()
