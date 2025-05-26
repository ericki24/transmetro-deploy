from django.shortcuts import render, redirect, get_object_or_404
from .models import Linea
from .forms import LineaForm
from django.contrib import messages
from lineaestacion.models import LineaEstacion
from buses.models import Bus
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('lineas.view_linea', raise_exception=True)
def lista_lineas(request):
    query = request.GET.get('q', '').strip()
    lineas = Linea.objects.all()

    if query:
        lineas = lineas.filter(nombre__icontains=query)

    return render(request, 'lineas/lista.html', {
        'lineas': lineas,
        'query': query
    })

@login_required
@permission_required('lineas.add_linea', raise_exception=True)
def crear_linea(request):
    form = LineaForm(request.POST or None)
    if form.is_valid():
        nueva = form.save()
        messages.success(request, f"✅ Línea '{nueva.nombre}' creada exitosamente.")
        return redirect('lista_lineas')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'lineas/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('lineas.change_linea', raise_exception=True)
def editar_linea(request, pk):
    linea = get_object_or_404(Linea, pk=pk)
    form = LineaForm(request.POST or None, instance=linea)
    if form.is_valid():
        form.save()
        messages.success(request, f"✅ Línea '{linea.nombre}' actualizada correctamente.")
        return redirect('lista_lineas')
    elif request.method == "POST":
        messages.error(request, "⚠️ Hubo un error al actualizar los datos.")
    return render(request, 'lineas/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('lineas.delete_linea', raise_exception=True)
def eliminar_linea(request, pk):
    linea = get_object_or_404(Linea, pk=pk)

    if LineaEstacion.objects.filter(id_linea=linea).exists():
        messages.error(request, f"❌ No se puede eliminar la línea '{linea.nombre}' porque tiene estaciones asignadas.")
        return redirect('lista_lineas')

    if Bus.objects.filter(id_linea=linea).exists():
        messages.error(request, f"❌ No se puede eliminar la línea '{linea.nombre}' porque tiene buses asignados.")
        return redirect('lista_lineas')

    try:
        linea.delete()
        messages.success(request, f"🗑️ Línea '{linea.nombre}' eliminada correctamente.")
    except:
        messages.error(request, "❌ Ocurrió un error inesperado al intentar eliminar la línea.")
    return redirect('lista_lineas')
