from django.shortcuts import render, redirect, get_object_or_404
from .models import Acceso
from .forms import AccesoForm
from guardias.models import Guardia
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('accesos.view_acceso', raise_exception=True)
def lista_accesos(request):
    query = request.GET.get('q', '').strip()
    accesos = Acceso.objects.select_related('id_estacion').all()

    if query:
        accesos = accesos.filter(descripcion__icontains=query)

    return render(request, 'accesos/lista.html', {
        'accesos': accesos,
        'query': query
    })

@login_required
@permission_required('accesos.add_acceso', raise_exception=True)
def crear_acceso(request):
    form = AccesoForm(request.POST or None)
    if form.is_valid():
        acceso = form.save()
        messages.success(request, f"✅ Acceso '{acceso.descripcion or acceso.id_acceso}' creado correctamente. Ahora asignale al menos un guardia.")
        return redirect('crear_guardia')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'accesos/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('accesos.change_acceso', raise_exception=True)
def editar_acceso(request, pk):
    acceso = get_object_or_404(Acceso, pk=pk)
    form = AccesoForm(request.POST or None, instance=acceso)
    if form.is_valid():
        form.save()
        messages.success(request, f"✅ Acceso '{acceso.descripcion or acceso.id_acceso}' actualizado correctamente.")
        return redirect('lista_accesos')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'accesos/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('accesos.delete_acceso', raise_exception=True)
def eliminar_acceso(request, pk):
    acceso = get_object_or_404(Acceso, pk=pk)
    if Guardia.objects.filter(id_acceso=acceso).exists():
        messages.error(request, f"❌ No se puede eliminar el acceso '{acceso.descripcion or acceso.id_acceso}' porque tiene guardias asignados.")
        return redirect('lista_accesos')

    try:
        acceso.delete()
        messages.success(request, f"🗑️ Acceso '{acceso.descripcion or acceso.id_acceso}' eliminado correctamente.")
    except Exception:
        messages.error(request, "❌ Ocurrió un error inesperado al intentar eliminar este acceso.")
    return redirect('lista_accesos')

