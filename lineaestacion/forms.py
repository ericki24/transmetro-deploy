from django import forms
from .models import LineaEstacion

class LineaEstacionForm(forms.ModelForm):
    class Meta:
        model = LineaEstacion
        fields = ['id_linea', 'id_estacion', 'orden', 'distancia_a_siguiente']
        labels = {
            'id_linea': 'Línea',
            'id_estacion': 'Estación',
            'orden': 'Orden en la ruta',
            'distancia_a_siguiente': 'Distancia a la siguiente estación (km)'
        }
        widgets = {
            'orden': forms.NumberInput(attrs={'min': 1}),
            'distancia_a_siguiente': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        linea = cleaned_data.get('id_linea')
        estacion = cleaned_data.get('id_estacion')
        orden = cleaned_data.get('orden')
        distancia = cleaned_data.get('distancia_a_siguiente')

        if orden and orden < 1:
            self.add_error('orden', "El orden debe ser mayor o igual a 1.")

        if distancia is not None and distancia < 0:
            self.add_error('distancia_a_siguiente', "La distancia no puede ser negativa.")

        # Evitar duplicados
        if linea and estacion:
            qs = LineaEstacion.objects.filter(id_linea=linea, id_estacion=estacion)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Esta estación ya está asignada a esta línea.")

        return cleaned_data
