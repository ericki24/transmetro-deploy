from django.shortcuts import render, redirect, get_object_or_404
from .models import BusPiloto
from .forms import BusPilotoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('buspiloto.view_buspiloto', raise_exception=True)
def lista_buspiloto(request):
    relaciones = BusPiloto.objects.select_related('id_bus', 'id_piloto').all()
    return render(request, 'buspiloto/lista.html', {'relaciones': relaciones})

@login_required
@permission_required('buspiloto.add_buspiloto', raise_exception=True)
def crear_buspiloto(request):
    form = BusPilotoForm(request.POST or None)
    if form.is_valid():
        asignacion = form.save()
        messages.success(
            request,
            f"✅ Bus '{asignacion.id_bus.placa}' asignado al piloto '{asignacion.id_piloto.nombre}'."
        )
        return redirect('lista_buspiloto')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'buspiloto/formulario.html', {'form': form, 'accion': 'Asignar'})

@login_required
@permission_required('buspiloto.change_buspiloto', raise_exception=True)
def editar_buspiloto(request, pk):
    relacion = get_object_or_404(BusPiloto, pk=pk)
    form = BusPilotoForm(request.POST or None, instance=relacion)
    if form.is_valid():
        actualizado = form.save()
        messages.success(
            request,
            f"✏️ Asignación actualizada: Bus '{actualizado.id_bus.placa}' con piloto '{actualizado.id_piloto.nombre}'."
        )
        return redirect('lista_buspiloto')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'buspiloto/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('buspiloto.delete_buspiloto', raise_exception=True)
def eliminar_buspiloto(request, pk):
    relacion = get_object_or_404(BusPiloto, pk=pk)
    try:
        relacion.delete()
        messages.success(request, "🗑️ Asignación eliminada correctamente.")
    except:
        messages.error(request, "❌ No se puede eliminar esta asignación.")
    return redirect('lista_buspiloto')

