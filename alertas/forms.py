from django import forms
from .models import Alerta

class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        fields = ['mensaje', 'id_estacion', 'fecha']
        labels = {
            'mensaje': 'Mensaje de alerta',
            'id_estacion': 'Estación asociada',
            'fecha': 'Fecha de incidente',
        }

        widgets = {
            'fecha': forms.SelectDateWidget(empty_label=("Año", "Mes", "Día")),
        }

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        if not mensaje:
            raise forms.ValidationError("El mensaje no puede estar vacío.")
        return mensaje

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if not fecha:
            raise forms.ValidationError("Debe seleccionar una fecha.")
        return fecha
