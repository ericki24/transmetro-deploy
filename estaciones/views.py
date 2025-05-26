from django.shortcuts import render, redirect, get_object_or_404
from .models import Estacion
from .forms import EstacionForm
from django.contrib import messages
from lineaestacion.models import LineaEstacion
from accesos.models import Acceso
from parqueos.models import Parqueo
from operadores.models import Operador
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('estaciones.view_estacion', raise_exception=True)
def lista_estaciones(request):
    query = request.GET.get('q', '').strip()
    estaciones = Estacion.objects.all()

    if query:
        estaciones = estaciones.filter(nombre__icontains=query)

    return render(request, 'estaciones/lista.html', {
        'estaciones': estaciones,
        'query': query
    })

@login_required
@permission_required('estaciones.add_estacion', raise_exception=True)
def crear_estacion(request):
    form = EstacionForm(request.POST or None)
    if form.is_valid():
        estacion = form.save()
        messages.success(request, f"✅ Estación '{estacion.nombre}' creada en la municipalidad '{estacion.id_municipalidad.nombre}'.")
        return redirect('lista_estaciones')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor completá todos los campos obligatorios correctamente.")
    return render(request, 'estaciones/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('estaciones.change_estacion', raise_exception=True)
def editar_estacion(request, pk):
    estacion = get_object_or_404(Estacion, pk=pk)
    form = EstacionForm(request.POST or None, instance=estacion)
    if form.is_valid():
        form.save()
        messages.success(request, f"✅ Estación '{estacion.nombre}' actualizada correctamente.")
        return redirect('lista_estaciones')
    elif request.method == "POST":
        messages.error(request, "⚠️ Hubo un error al actualizar. Verificá los datos ingresados.")
    return render(request, 'estaciones/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('estaciones.delete_estacion', raise_exception=True)
def eliminar_estacion(request, pk):
    estacion = get_object_or_404(Estacion, pk=pk)

    if Acceso.objects.filter(id_estacion=estacion).exists():
        messages.error(request, f"❌ No se puede eliminar la estación '{estacion.nombre}' porque tiene accesos asignados.")
        return redirect('lista_estaciones')

    if Parqueo.objects.filter(id_estacion=estacion).exists():
        messages.error(request, f"❌ No se puede eliminar la estación '{estacion.nombre}' porque tiene parqueos asignados.")
        return redirect('lista_estaciones')

    if Operador.objects.filter(id_estacion=estacion).exists():
        messages.error(request, f"❌ No se puede eliminar la estación '{estacion.nombre}' porque tiene un operador asignado.")
        return redirect('lista_estaciones')

    lineas_relacionadas = LineaEstacion.objects.filter(id_estacion=estacion)
    for relacion in lineas_relacionadas:
        total_estaciones = LineaEstacion.objects.filter(id_linea=relacion.id_linea).count()
        if total_estaciones <= 1:
            messages.error(request, f"❌ No se puede eliminar la estación '{estacion.nombre}' porque es la única en la línea '{relacion.id_linea.nombre}'.")
            return redirect('lista_estaciones')

    try:
        estacion.delete()
        messages.success(request, f"🗑️ Estación '{estacion.nombre}' eliminada correctamente.")
    except:
        messages.error(request, "❌ No se puede eliminar esta estación porque está en uso.")
    return redirect('lista_estaciones')

