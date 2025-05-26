# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Guardia
from .forms import GuardiaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('guardias.view_guardia', raise_exception=True)
def lista_guardias(request):
    query = request.GET.get('q', '').strip()
    guardias = Guardia.objects.select_related('id_acceso').all()

    if query:
        guardias = guardias.filter(nombre__icontains=query)

    return render(request, 'guardias/lista.html', {
        'guardias': guardias,
        'query': query
    })

@login_required
@permission_required('guardias.add_guardia', raise_exception=True)
def crear_guardia(request):
    form = GuardiaForm(request.POST or None)
    if form.is_valid():
        form.save()
        nuevo_guardia = form.save()
        messages.success(request, f"✅ Guardia '{nuevo_guardia.nombre}' creado exitosamente.")
        return redirect('lista_guardias')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'guardias/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('guardias.change_guardia', raise_exception=True)
def editar_guardia(request, pk):
    guardia = get_object_or_404(Guardia, pk=pk)
    form = GuardiaForm(request.POST or None, instance=guardia)
    if form.is_valid():
        form.save()
        messages.success(request, f"✅ Guardia '{guardia.nombre}' actualizado correctamente.")
        return redirect('lista_guardias')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor corregí los errores del formulario.")
    return render(request, 'guardias/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('guardias.delete_guardia', raise_exception=True)
def eliminar_guardia(request, pk):
    guardia = get_object_or_404(Guardia, pk=pk)
    total_guardias = Guardia.objects.filter(id_acceso=guardia.id_acceso).count()


    if total_guardias <= 1:
        messages.error(request, f"❌ No se puede eliminar al último guardia del acceso '{guardia.id_acceso.descripcion or guardia.id_acceso.id_acceso}'.")
        return redirect('lista_guardias')


    try:
        guardia.delete()
        messages.success(request, f"🗑️ Guardia '{guardia.nombre}' eliminado correctamente.")
    except Exception:
        messages.error(request, "❌ Ocurrió un error al intentar eliminar este guardia. Verificá si está en uso.")
    return redirect('lista_guardias')
