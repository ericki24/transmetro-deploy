from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse
from django.db.models import Q
import pandas as pd
from io import BytesIO
from django.utils.timezone import now
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required



def obtener_datos_formateados(model_class, queryset):
    data = []
    for obj in queryset.select_related():
        fila = {}
        for field in model_class._meta.fields:
            valor = getattr(obj, field.name)
            if field.is_relation and hasattr(valor, '__str__'):
                fila[field.verbose_name] = str(valor)
            else:
                fila[field.verbose_name] = valor
        data.append(fila)
    return data

MODELOS_REPORTE = {
    'municipalidad': 'municipios.Municipalidad',
    'linea': 'lineas.Linea',
    'estacion': 'estaciones.Estacion',
    'acceso': 'accesos.Acceso',
    'guardia': 'guardias.Guardia',
    'parqueo': 'parqueos.Parqueo',
    'bus': 'buses.Bus',
    'piloto': 'pilotos.Piloto',
    'operador': 'operadores.Operador',
    'alerta': 'alertas.Alerta',
    'lineaestacion': 'lineaestacion.LineaEstacion',
    'buspiloto': 'buspiloto.BusPiloto',
}

@login_required
def reporte_general(request):
    modelo_seleccionado = request.GET.get('modelo')
    data = []
    campos = []
    nombre_modelo = ''

    lineas = parqueos = municipalidades = estaciones = accesos = buses = pilotos = []
    id_linea = request.GET.get('linea')
    id_parqueo = request.GET.get('parqueo')
    id_muni = request.GET.get('municipalidad')
    id_estacion = request.GET.get('estacion')
    id_bus = request.GET.get('bus')
    id_piloto = request.GET.get('piloto')

    if modelo_seleccionado in MODELOS_REPORTE:
        app_model = MODELOS_REPORTE[modelo_seleccionado]
        model_class = apps.get_model(app_model)
        nombre_modelo = model_class._meta.verbose_name_plural.title()
        queryset = model_class.objects.all()

        filtro = request.GET.get('filtro', '').strip()
        if filtro:
            q = Q()
            for field in model_class._meta.fields:
                if 'nombre' in field.name or 'placa' in field.name:
                    q |= Q(**{f"{field.name}__icontains": filtro})
            queryset = queryset.filter(q)

        if modelo_seleccionado == 'bus':
            from lineas.models import Linea
            from parqueos.models import Parqueo
            lineas = Linea.objects.all()
            parqueos = Parqueo.objects.all()
            if id_linea:
                queryset = queryset.filter(id_linea=id_linea)
            if id_parqueo:
                queryset = queryset.filter(id_parqueo=id_parqueo)

        elif modelo_seleccionado == 'estacion':
            from municipios.models import Municipalidad
            municipalidades = Municipalidad.objects.all()
            if id_muni:
                queryset = queryset.filter(id_municipalidad=id_muni)

        elif modelo_seleccionado == 'acceso':
            from estaciones.models import Estacion
            estaciones = Estacion.objects.all()
            if id_estacion:
                queryset = queryset.filter(id_estacion=id_estacion)

        

        elif modelo_seleccionado == 'guardia':
            from accesos.models import Acceso
            accesos = Acceso.objects.all()
            id_acceso = request.GET.get('acceso')
            if id_acceso:
                queryset = queryset.filter(id_acceso=id_acceso)


        elif modelo_seleccionado == 'lineaestacion':
            from lineas.models import Linea
            from estaciones.models import Estacion
            lineas = Linea.objects.all()
            estaciones = Estacion.objects.all()
            if id_linea:
                queryset = queryset.filter(id_linea=id_linea)
            if id_estacion:
                queryset = queryset.filter(id_estacion=id_estacion)

        elif modelo_seleccionado == 'buspiloto':
            from buses.models import Bus
            from pilotos.models import Piloto
            buses = Bus.objects.all()
            pilotos = Piloto.objects.all()
            if id_bus:
                queryset = queryset.filter(id_bus=id_bus)
            if id_piloto:
                queryset = queryset.filter(id_piloto=id_piloto)

        campos = [f.verbose_name for f in model_class._meta.fields]
        data = obtener_datos_formateados(model_class, queryset)

    context = {
        'modelos': MODELOS_REPORTE.keys(),
        'modelo_seleccionado': modelo_seleccionado,
        'nombre_modelo': nombre_modelo,
        'data': data,
        'campos': campos,
        'lineas': lineas,
        'parqueos': parqueos,
        'municipalidades': municipalidades,
        'estaciones': estaciones,
        'accesos': accesos,
        'buses': buses,
        'pilotos': pilotos,
        'filtro_linea': id_linea,
        'filtro_parqueo': id_parqueo,
        'filtro_muni': id_muni,
        'filtro_estacion': id_estacion,
        'filtro_bus': id_bus,
        'filtro_piloto': id_piloto,
        'filtro_general': request.GET.get('filtro', '')
    }
    return render(request, 'reportes/reporte_general.html', context)

@login_required
def exportar_excel(request):
    modelo = request.GET.get('modelo')
    filtro = request.GET.get('filtro', '').strip()

    if not modelo or modelo not in MODELOS_REPORTE:
        return HttpResponse("Modelo no válido", status=400)

    model_class = apps.get_model(MODELOS_REPORTE[modelo])
    queryset = model_class.objects.all()

    if filtro:
        q = Q()
        for field in model_class._meta.fields:
            if 'nombre' in field.name or 'placa' in field.name:
                q |= Q(**{f"{field.name}__icontains": filtro})
        queryset = queryset.filter(q)

    data = obtener_datos_formateados(model_class, queryset)
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte')

    output.seek(0)
    filename = f'reporte_{modelo}_{now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def exportar_pdf(request):
    modelo = request.GET.get('modelo')
    filtro = request.GET.get('filtro', '').strip()

    if not modelo or modelo not in MODELOS_REPORTE:
        return HttpResponse("Modelo no válido", status=400)

    model_class = apps.get_model(MODELOS_REPORTE[modelo])
    queryset = model_class.objects.all()

    if filtro:
        q = Q()
        for field in model_class._meta.fields:
            if 'nombre' in field.name or 'placa' in field.name:
                q |= Q(**{f"{field.name}__icontains": filtro})
        queryset = queryset.filter(q)

    campos = [f.verbose_name for f in model_class._meta.fields]
    data = obtener_datos_formateados(model_class, queryset)

    html = render_to_string("reportes/reporte_pdf.html", {
        'nombre_modelo': model_class._meta.verbose_name_plural.title(),
        'fecha': now().strftime("%d/%m/%Y %H:%M"),
        'campos': campos,
        'data': data,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{modelo}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response
