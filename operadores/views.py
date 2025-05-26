from django.shortcuts import render, redirect, get_object_or_404
from .models import Operador
from .forms import OperadorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('operadores.view_operador', raise_exception=True)
def lista_operadores(request):
    query = request.GET.get('q', '').strip()
    operadores = Operador.objects.select_related('id_estacion').all()

    if query:
        operadores = operadores.filter(nombre__icontains=query)

    return render(request, 'operadores/lista.html', {
        'operadores': operadores,
        'query': query
    })

@login_required
@permission_required('operadores.add_operador', raise_exception=True)
def crear_operador(request):
    form = OperadorForm(request.POST or None)
    if form.is_valid():
        nuevo = form.save()
        nombre = nuevo.nombre or "sin nombre"
        messages.success(
            request,
            f"✅ Operador '{nombre}' asignado a la estación '{nuevo.id_estacion.nombre}'."
        )
        return redirect('lista_operadores')
    elif request.method == "POST":
        messages.error(request, "⚠️ Revisá los datos ingresados.")
    return render(request, 'operadores/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('operadores.change_operador', raise_exception=True)
def editar_operador(request, pk):
    operador = get_object_or_404(Operador, pk=pk)
    form = OperadorForm(request.POST or None, instance=operador)
    if form.is_valid():
        actualizado = form.save()
        messages.success(
            request,
            f"✏️ Operador '{actualizado.nombre or 'sin nombre'}' actualizado correctamente."
        )
        return redirect('lista_operadores')
    elif request.method == "POST":
        messages.error(request, "⚠️ Hubo un error al actualizar los datos.")
    return render(request, 'operadores/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('operadores.delete_operador', raise_exception=True)
def eliminar_operador(request, pk):
    operador = get_object_or_404(Operador, pk=pk)
    try:
        operador.delete()
        messages.success(request, "🗑️ Operador eliminado correctamente.")
    except:
        messages.error(request, "❌ No se puede eliminar este operador porque está en uso.")
    return redirect('lista_operadores')

