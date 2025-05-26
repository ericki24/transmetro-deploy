from django import forms
from .models import BusPiloto

class BusPilotoForm(forms.ModelForm):
    class Meta:
        model = BusPiloto
        fields = ['id_bus', 'id_piloto']
        labels = {
            'id_bus': 'Bus asignado',
            'id_piloto': 'Piloto asignado'
        }

    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get('id_bus')
        piloto = cleaned_data.get('id_piloto')

        if bus and BusPiloto.objects.filter(id_bus=bus).exclude(pk=self.instance.pk).exists():
            self.add_error('id_bus', "Este bus ya tiene un piloto asignado.")

        if piloto and BusPiloto.objects.filter(id_piloto=piloto).exclude(pk=self.instance.pk).exists():
            self.add_error('id_piloto', "Este piloto ya está asignado a otro bus.")

        return cleaned_data
