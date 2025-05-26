from django.shortcuts import render
from django.http import JsonResponse
from estaciones.models import Estacion
from lineas.models import Linea
from lineaestacion.models import LineaEstacion
import random
from django.contrib.auth.decorators import login_required

@login_required
def ver_mapa(request):
    return render(request, 'mapa/mapa.html')

@login_required
def datos_mapa(request):
    estaciones = Estacion.objects.exclude(latitud__isnull=True, longitud__isnull=True)

    # Crear un diccionario para obtener el color principal por estación
    estaciones_colores = {}
    relaciones = LineaEstacion.objects.select_related('id_linea', 'id_estacion')
    for rel in relaciones:
        est = rel.id_estacion
        linea = rel.id_linea
        if est.id_estacion not in estaciones_colores:
            estaciones_colores[est.id_estacion] = linea.color or '#3388ff'

    # Datos para marcadores con simulación de ocupación
    datos_estaciones = []
    for est in estaciones:
        capacidad = est.capacidad or 0
        ocupacion = random.randint(int(capacidad * 0.5), int(capacidad * 2)) if capacidad > 0 else 0
        sobrecupo = ocupacion > capacidad * 1.5 if capacidad > 0 else False
        color = estaciones_colores.get(est.id_estacion, '#3388ff')
        datos_estaciones.append({
            'nombre': est.nombre,
            'latitud': float(est.latitud),
            'longitud': float(est.longitud),
            'municipalidad': est.id_municipalidad.nombre,
            'capacidad': capacidad,
            'ocupacion': ocupacion,
            'sobrecupo': sobrecupo,
            'color': color
        })

    # Datos para líneas (polilíneas con color)
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

    return JsonResponse({
        'estaciones': datos_estaciones,
        'rutas': rutas_lineas
    })
