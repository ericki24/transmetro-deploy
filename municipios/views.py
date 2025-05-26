from django.shortcuts import render, redirect, get_object_or_404
from .models import Municipalidad
from .forms import MunicipalidadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from lineas.models import Linea
from estaciones.models import Estacion

@login_required
@permission_required('municipios.view_municipalidad', raise_exception=True)
def lista_municipios(request):
    query = request.GET.get('q', '').strip()
    municipios = Municipalidad.objects.all()

    if query:
        municipios = municipios.filter(nombre__icontains=query)

    return render(request, 'municipios/lista.html', {
        'municipios': municipios,
        'query': query
    })

@login_required
@permission_required('municipios.add_municipalidad', raise_exception=True)
def crear_municipio(request):
    form = MunicipalidadForm(request.POST or None)
    if form.is_valid():
        nuevo = form.save()
        messages.success(request, f"✅ Municipalidad '{nuevo.nombre}' creada exitosamente.")
        return redirect('lista_municipios')
    elif request.method == "POST":
        messages.error(request, "⚠️ Por favor revisá los datos ingresados.")
    return render(request, 'municipios/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@permission_required('municipios.change_municipalidad', raise_exception=True)
def editar_municipio(request, pk):
    municipio = get_object_or_404(Municipalidad, pk=pk)
    form = MunicipalidadForm(request.POST or None, instance=municipio)
    if form.is_valid():
        form.save()
        messages.success(request, f"✅ Municipalidad '{municipio.nombre}' actualizada correctamente.")
        return redirect('lista_municipios')
    elif request.method == "POST":
        messages.error(request, "⚠️ Hubo un error al intentar actualizar los datos.")
    return render(request, 'municipios/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@permission_required('municipios.delete_municipalidad', raise_exception=True)
def eliminar_municipio(request, pk):
    municipio = get_object_or_404(Municipalidad, pk=pk)

    if Linea.objects.filter(id_municipalidad=municipio).exists() or Estacion.objects.filter(id_municipalidad=municipio).exists():
        messages.error(request, f"❌ No se puede eliminar la municipalidad '{municipio.nombre}' porque tiene líneas o estaciones asociadas.")
        return redirect('lista_municipios')

    try:
        municipio.delete()
        messages.success(request, f"🗑️ Municipalidad '{municipio.nombre}' eliminada correctamente.")
    except:
        messages.error(request, "❌ Error inesperado al eliminar la municipalidad.")
    return redirect('lista_municipios')
