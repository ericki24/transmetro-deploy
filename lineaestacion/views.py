from django.shortcuts import render, redirect, get_object_or_404
from .models import LineaEstacion
from .forms import LineaEstacionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('lineaestacion.view_lineaestacion', raise_exception=True)
def lista_lineaestacion(request):
    registros = LineaEstacion.objects.select_related('id_linea', 'id_estacion').all().order_by('id_linea', 'orden')
    return render(request, 'lineaestacion/lista.html', {'registros': registros})

@login_required
@permission_required('lineaestacion.add_lineaestacion', raise_exception=True)
def crear_lineaestacion(request):
    form = LineaEstacionForm(request.POST or None)
    if form.is_valid():
        registro = form.save()
        messages.success(
            request,
            f"✅ Estación '{registro.id_estacion.nombre}' asignada a la línea '{registro.id_linea.nombre}' en el orden {registro.orden}."
        )
        return redirect('lista_lineaestacion')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'lineaestacion/formulario.html', {'form': form, 'accion': 'Asignar'})

@login_required
@permission_required('lineaestacion.change_lineaestacion', raise_exception=True)
def editar_lineaestacion(request, pk):
    registro = get_object_or_404(LineaEstacion, pk=pk)
    form = LineaEstacionForm(request.POST or None, instance=registro)
    if form.is_valid():
        actualizado = form.save()
        messages.success(
            request,
            f"✏️ Asignación actualizada: '{actualizado.id_estacion.nombre}' en línea '{actualizado.id_linea.nombre}' (Orden {actualizado.orden})."
        )
        return redirect('lista_lineaestacion')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'lineaestacion/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('lineaestacion.delete_lineaestacion', raise_exception=True)
def eliminar_lineaestacion(request, pk):
    registro = get_object_or_404(LineaEstacion, pk=pk)
    try:
        registro.delete()
        messages.success(request, f"🗑️ Estación '{registro.id_estacion.nombre}' eliminada de la línea '{registro.id_linea.nombre}'.")
    except:
        messages.error(request, "❌ No se puede eliminar esta asignación porque está en uso.")
    return redirect('lista_lineaestacion')

