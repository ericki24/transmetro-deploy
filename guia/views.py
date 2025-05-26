
from django.shortcuts import render
from django.http import JsonResponse
from estaciones.models import Estacion
from lineas.models import Linea
from lineaestacion.models import LineaEstacion
import random

def ver_guia(request):
    return render(request, 'guia/guia.html')

from django.http import JsonResponse
from estaciones.models import Estacion
from lineas.models import Linea
from lineaestacion.models import LineaEstacion
import random

def datos_guia(request):
    estaciones = Estacion.objects.exclude(latitud__isnull=True, longitud__isnull=True)
    relaciones = LineaEstacion.objects.select_related('id_linea', 'id_estacion')
    estaciones_lineas = {}

    # Mapeo de cada estación a su línea (tomando la primera si pertenece a varias)
    for rel in relaciones:
        est = rel.id_estacion
        linea = rel.id_linea
        if est.id_estacion not in estaciones_lineas:
            estaciones_lineas[est.id_estacion] = {
                'color': linea.color or '#3388ff',
                'nombre': linea.nombre
            }

    datos_estaciones = []
    for est in estaciones:
        capacidad = est.capacidad or 0
        ocupacion = random.randint(int(capacidad * 0.5), int(capacidad * 2)) if capacidad > 0 else 0
        sobrecupo = ocupacion > capacidad * 1.5 if capacidad > 0 else False
        linea_info = estaciones_lineas.get(est.id_estacion, {'color': '#3388ff', 'nombre': 'Sin línea'})

        datos_estaciones.append({
            'nombre': est.nombre,
            'latitud': float(est.latitud),
            'longitud': float(est.longitud),
            'municipalidad': est.id_municipalidad.nombre,
            'capacidad': capacidad,
            'ocupacion': ocupacion,
            'sobrecupo': sobrecupo,
            'color': linea_info['color'],
            'linea': linea_info['nombre']
        })

    rutas_lineas = []
    for linea in Linea.objects.all():
        estaciones_linea = LineaEstacion.objects.filter(id_linea=linea).select_related('id_estacion').order_by('orden')
        coordenadas = []
        for rel in estaciones_linea:
            est = rel.id_estacion
            if est.latitud and est.longitud:
                coordenadas.append([float(est.latitud), float(est.longitud)])
        if coordenadas:
            rutas_lineas.append({
                'nombre': linea.nombre,
                'color': linea.color or '#3388ff',
                'coordenadas': coordenadas
            })

    return JsonResponse({'estaciones': datos_estaciones, 'rutas': rutas_lineas})
