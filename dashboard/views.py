from django.shortcuts import render
from alertas.models import Alerta
from buses.models import Bus
from buspiloto.models import BusPiloto
from estaciones.models import Estacion
from municipios.models import Municipalidad
from lineas.models import Linea
from lineaestacion.models import LineaEstacion
import random
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    # Evitar duplicar alertas cada vez: eliminamos las generadas automáticamente (si querés)
    Alerta.objects.filter(mensaje__in=["se necesita bus", "esperar 5 minutos más"]).delete()

    # Alertas reales (ya creadas manualmente)
    total_alertas = Alerta.objects.count()

    # Buses sin piloto
    buses_con_piloto = BusPiloto.objects.values_list('id_bus', flat=True)
    buses_sin_piloto = Bus.objects.exclude(id_bus__in=buses_con_piloto).count()

    # Buses por línea
    buses_por_linea = [
        {'linea': linea.nombre, 'total': Bus.objects.filter(id_linea=linea).count()}
        for linea in Linea.objects.all()
    ]

    # Estaciones por municipalidad
    estaciones_por_muni = [
        {'municipalidad': muni.nombre, 'total': Estacion.objects.filter(id_municipalidad=muni).count()}
        for muni in Municipalidad.objects.all()
    ]

    # Estaciones con sobrecupo (simulado y alerta real)
    estaciones_sobrecupo = []
    for estacion in Estacion.objects.all():
        capacidad = estacion.capacidad or 0
        ocupacion_simulada = random.randint(int(capacidad * 0.5), int(capacidad * 2)) if capacidad > 0 else 0
        if capacidad > 0 and ocupacion_simulada > capacidad * 1.5:
            estaciones_sobrecupo.append({
                'nombre': estacion.nombre,
                'capacidad': capacidad,
                'ocupacion': ocupacion_simulada
            })
            Alerta.objects.create(
                mensaje="se necesita bus",
                fecha=timezone.now(),
                id_estacion=estacion
            )

    # Buses con baja ocupación (simulado y alerta real)
    buses_baja_ocupacion = []
    for bus in Bus.objects.select_related('id_linea').all():
        capacidad = bus.capacidad or 0
        pasajeros_simulados = random.randint(0, capacidad) if capacidad > 0 else 0
        if capacidad > 0 and pasajeros_simulados < capacidad * 0.25:
            buses_baja_ocupacion.append({
                'placa': bus.placa,
                'capacidad': capacidad,
                'ocupacion': pasajeros_simulados
            })

            # Vincular con estación de la línea (solo si hay al menos una estación)
            estaciones_linea = LineaEstacion.objects.filter(id_linea=bus.id_linea).order_by('orden')
            if estaciones_linea.exists():
                estacion_destino = estaciones_linea.first().id_estacion
                Alerta.objects.create(
                    mensaje="esperar 5 minutos más",
                    fecha=timezone.now(),
                    id_estacion=estacion_destino
                )


           


    context = {
        'total_alertas': Alerta.objects.count(),
        'buses_sin_piloto': buses_sin_piloto,
        'buses_por_linea': buses_por_linea,
        'estaciones_por_muni': estaciones_por_muni,
        'estaciones_sobrecupo': estaciones_sobrecupo,
        'buses_baja_ocupacion': buses_baja_ocupacion,
    }


# Agregar alertas recientes al contexto
    alertas = Alerta.objects.select_related('id_estacion').order_by('-fecha')[:20]
    context['alertas'] = alertas



    return render(request, 'dashboard/home.html', context)
