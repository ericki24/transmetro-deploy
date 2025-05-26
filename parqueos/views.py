from django.shortcuts import render, redirect, get_object_or_404
from .models import Parqueo
from .forms import ParqueoForm
from buses.models import Bus
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('parqueos.view_parqueo', raise_exception=True)
def lista_parqueos(request):
    query = request.GET.get('q', '').strip()
    parqueos = Parqueo.objects.select_related('id_estacion').all()

    if query:
        parqueos = parqueos.filter(direccion__icontains=query)

    return render(request, 'parqueos/lista.html', {
        'parqueos': parqueos,
        'query': query
    })

@login_required
@permission_required('parqueos.add_parqueo', raise_exception=True)
def crear_parqueo(request):
    form = ParqueoForm(request.POST or None)
    if form.is_valid():
        parqueo = form.save()
        messages.success(request, f"✅ Parqueo creado en estación '{parqueo.id_estacion.nombre}'.")
        return redirect('lista_parqueos')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'parqueos/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('parqueos.change_parqueo', raise_exception=True)
def editar_parqueo(request, pk):
    parqueo = get_object_or_404(Parqueo, pk=pk)
    form = ParqueoForm(request.POST or None, instance=parqueo)
    if form.is_valid():
        form.save()
        messages.success(request, f"✅ Parqueo actualizado (Estación: {parqueo.id_estacion.nombre}).")
        return redirect('lista_parqueos')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'parqueos/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('parqueos.delete_parqueo', raise_exception=True)
def eliminar_parqueo(request, pk):
    parqueo = get_object_or_404(Parqueo, pk=pk)

    if Bus.objects.filter(id_parqueo=parqueo).exists():
        messages.error(request, f"❌ No se puede eliminar el parqueo asignado a '{parqueo.id_estacion.nombre}' porque tiene buses relacionados.")
        return redirect('lista_parqueos')

    try:
        parqueo.delete()
        messages.success(request, f"🗑️ Parqueo eliminado correctamente.")
    except:
        messages.error(request, "❌ Ocurrió un error inesperado al intentar eliminar este parqueo.")
    return redirect('lista_parqueos')

