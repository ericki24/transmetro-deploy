from django import forms

from lineaestacion.models import LineaEstacion
from .models import Bus

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['placa', 'capacidad', 'id_linea', 'id_parqueo']
        labels = {
            'placa': 'Placa del bus',
            'capacidad': 'Capacidad máxima',
            'id_linea': 'Línea asignada (opcional)',
            'id_parqueo': 'Parqueo asignado'
        }
        widgets = {
            'capacidad': forms.NumberInput(attrs={'min': 1}),
        }

    def clean_placa(self):
        placa = self.cleaned_data['placa'].strip().upper()
        buses = Bus.objects.all()
        if self.instance.pk:
            buses = buses.exclude(pk=self.instance.pk)
        if buses.filter(placa__iexact=placa).exists():
            raise forms.ValidationError("Ya existe un bus con esta placa.")
        return placa

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad is None or capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser mayor a 0.")
        return capacidad

    def clean_id_parqueo(self):
        parqueo = self.cleaned_data.get('id_parqueo')
        if not parqueo:
            raise forms.ValidationError("Debe seleccionar un parqueo.")
        return parqueo


    def clean_id_linea(self):
            linea = self.cleaned_data.get('id_linea')

            # si no se asignó línea, no validamos nada
            if not linea:
                return linea

            # contar estaciones de esta línea
            total_estaciones = LineaEstacion.objects.filter(id_linea=linea).count()

            if total_estaciones == 0:
                raise forms.ValidationError("No se puede asignar un bus a una línea que no tiene estaciones.")

            # contar buses ya asignados (excluyendo el actual si se está editando)
            buses = Bus.objects.filter(id_linea=linea)
            if self.instance.pk:
                buses = buses.exclude(pk=self.instance.pk)

            total_buses = buses.count() + 1  # sumamos el actual

            if total_buses < total_estaciones:
                raise forms.ValidationError(f"La línea necesita al menos {total_estaciones} buses (actual: {total_buses}).")

            if total_buses > total_estaciones * 2:
                raise forms.ValidationError(f"La línea no puede tener más de {total_estaciones * 2} buses (actual: {total_buses}).")

            return linea
