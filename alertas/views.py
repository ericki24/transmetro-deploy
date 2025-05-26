from django.shortcuts import render, redirect, get_object_or_404
from .models import Alerta
from .forms import AlertaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('alertas.view_alerta', raise_exception=True)
def lista_alertas(request):
    query = request.GET.get('q', '').strip()
    alertas = Alerta.objects.select_related('id_estacion').all()

    if query:
        alertas = alertas.filter(mensaje__icontains=query)

    return render(request, 'alertas/lista.html', {
        'alertas': alertas,
        'query': query
    })

@login_required
@permission_required('alertas.add_alerta', raise_exception=True)
def crear_alerta(request):
    form = AlertaForm(request.POST or None)
    if form.is_valid():
        nueva = form.save()
        messages.success(request, f"✅ Alerta creada para la estación '{nueva.id_estacion.nombre}'.")
        return redirect('lista_alertas')
    elif request.method == "POST":
        messages.error(request, "⚠️ Revisá los campos del formulario.")
    return render(request, 'alertas/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('alertas.change_alerta', raise_exception=True)
def editar_alerta(request, pk):
    alerta = get_object_or_404(Alerta, pk=pk)
    form = AlertaForm(request.POST or None, instance=alerta)
    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Alerta actualizada correctamente.")
        return redirect('lista_alertas')
    elif request.method == "POST":
        messages.error(request, "⚠️ Revisá los datos ingresados.")
    return render(request, 'alertas/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('alertas.delete_alerta', raise_exception=True)
def eliminar_alerta(request, pk):
    alerta = get_object_or_404(Alerta, pk=pk)
    try:
        alerta.delete()
        messages.success(request, "🗑️ Alerta eliminada correctamente.")
    except:
        messages.error(request, "❌ No se puede eliminar esta alerta porque está en uso.")
    return redirect('lista_alertas')

