from django.shortcuts import render, redirect, get_object_or_404
from .models import Bus
from .forms import BusForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('buses.view_bus', raise_exception=True)
def lista_buses(request):
    query = request.GET.get('q', '').strip()
    buses = Bus.objects.select_related('id_linea', 'id_parqueo').all()

    if query:
        buses = buses.filter(placa__icontains=query)

    return render(request, 'buses/lista.html', {
        'buses': buses,
        'query': query
    })

@login_required
@permission_required('buses.add_bus', raise_exception=True)
def crear_bus(request):
    form = BusForm(request.POST or None)
    if form.is_valid():
        bus = form.save()
        messages.success(request, f"✅ Bus con placa '{bus.placa}' creado exitosamente.")
        return redirect('lista_buses')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'buses/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('buses.change_bus', raise_exception=True)
def editar_bus(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    form = BusForm(request.POST or None, instance=bus)
    if form.is_valid():
        form.save()
        messages.success(request, f"✅ Bus '{bus.placa}' actualizado correctamente.")
        return redirect('lista_buses')
    elif request.method == "POST":
        messages.error(request, "⚠️ Hubo un error al actualizar el bus.")
    return render(request, 'buses/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('buses.delete_bus', raise_exception=True)
def eliminar_bus(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    try:
        bus.delete()
        messages.success(request, f"🗑️ Bus '{bus.placa}' eliminado correctamente.")
    except:
        messages.error(request, f"❌ No se puede eliminar el bus '{bus.placa}' porque está en uso.")
    return redirect('lista_buses')
