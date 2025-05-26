from django.shortcuts import render, redirect, get_object_or_404
from .models import Piloto
from .forms import PilotoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('pilotos.view_piloto', raise_exception=True)
def lista_pilotos(request):
    query = request.GET.get('q', '').strip()
    pilotos = Piloto.objects.all()

    if query:
        pilotos = pilotos.filter(nombre__icontains=query)

    return render(request, 'pilotos/lista.html', {
        'pilotos': pilotos,
        'query': query
    })

@login_required
@permission_required('pilotos.add_piloto', raise_exception=True)
def crear_piloto(request):
    form = PilotoForm(request.POST or None)
    if form.is_valid():
        nuevo = form.save()
        messages.success(request, f"✅ Piloto '{nuevo.nombre}' creado exitosamente.")
        return redirect('lista_pilotos')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor revisá los datos ingresados.")
    return render(request, 'pilotos/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('pilotos.change_piloto', raise_exception=True)
def editar_piloto(request, pk):
    piloto = get_object_or_404(Piloto, pk=pk)
    form = PilotoForm(request.POST or None, instance=piloto)
    if form.is_valid():
        form.save()
        messages.success(request, f"✅ Piloto '{piloto.nombre}' actualizado correctamente.")
        return redirect('lista_pilotos')
    elif request.method == "POST":
        messages.error(request, "⚠️ Hubo un error al actualizar los datos.")
    return render(request, 'pilotos/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('pilotos.delete_piloto', raise_exception=True)
def eliminar_piloto(request, pk):
    piloto = get_object_or_404(Piloto, pk=pk)
    try:
        piloto.delete()
        messages.success(request, f"🗑️ Piloto '{piloto.nombre}' eliminado correctamente.")
    except:
        messages.error(request, f"❌ No se puede eliminar al piloto '{piloto.nombre}' porque está en uso.")
    return redirect('lista_pilotos')

