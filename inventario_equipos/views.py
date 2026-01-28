from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Equipo, Mantenimiento, Red
from .forms import EquipoForm, MantenimientoForm, RedForm

# ==========================================
# NUEVO: MENÚ PRINCIPAL DEL MÓDULO
# ==========================================
def menu_inventario(request):
    """Esta vista carga las 3 opciones: Equipos, Mantenimientos y Redes"""
    return render(request, 'inventario_equipos/menu_inventario.html')

# ==========================================
# 1. SECCIÓN DE EQUIPOS
# ==========================================
def lista_equipos(request):
    equipos = Equipo.objects.all().order_by('-id')
    equipos_mantenimiento = Equipo.objects.filter(estado='mantenimiento')
    return render(request, 'inventario_equipos/equipo_list.html', {
        'equipos': equipos,
        'equipos_mantenimiento': equipos_mantenimiento
    })

def crear_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Equipo registrado exitosamente!')
            return redirect('lista_equipos')
        else:
            messages.error(request, 'Error al registrar el equipo. Revisa los campos obligatorios.')
            print("Errores en formulario Equipo:", form.errors)
    else:
        form = EquipoForm()
    return render(request, 'inventario_equipos/equipo_form.html', {'form': form, 'titulo': 'Registrar Nuevo Equipo'})

def editar_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipo actualizado correctamente.')
            return redirect('lista_equipos')
        else:
            messages.error(request, 'Error al actualizar el equipo. Revisa los datos.')
    else:
        form = EquipoForm(instance=equipo)
    return render(request, 'inventario_equipos/equipo_form.html', {'form': form, 'titulo': 'Editar Equipo'})

def eliminar_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == 'POST':
        equipo.delete()
        messages.success(request, 'Equipo eliminado.')
        return redirect('lista_equipos')
    return render(request, 'inventario_equipos/equipo_confirm_delete.html', {'equipo': equipo})


# ==========================================
# 2. SECCIÓN DE MANTENIMIENTOS
# ==========================================
def lista_mantenimientos(request):
    mantenimientos = Mantenimiento.objects.all().order_by('-fecha_mantenimiento')
    return render(request, 'inventario_equipos/mantenimiento_list.html', {'mantenimientos': mantenimientos})

def crear_mantenimiento(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mantenimiento registrado exitosamente.')
            return redirect('lista_mantenimientos')
        else:
            # --- CORRECCIÓN AQUÍ ---
            # Ahora el mensaje imprimirá el error técnico exacto en tu pantalla
            messages.error(request, f"FALLO AL GUARDAR: {form.errors}")
            print("Errores detallados:", form.errors)
    else:
        form = MantenimientoForm()
    return render(request, 'inventario_equipos/mantenimiento_form.html', {'form': form})

def editar_mantenimiento(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mantenimiento actualizado.')
            return redirect('lista_mantenimientos')
        else:
            messages.error(request, f"Error al actualizar: {form.errors}")
    else:
        form = MantenimientoForm(instance=mantenimiento)
    return render(request, 'inventario_equipos/mantenimiento_form.html', {'form': form})

def eliminar_mantenimiento(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)
    if request.method == 'POST':
        mantenimiento.delete()
        messages.success(request, 'Mantenimiento eliminado.')
        return redirect('lista_mantenimientos')
    return render(request, 'inventario_equipos/mantenimiento_confirm_delete.html', {'mantenimiento': mantenimiento})


# ==========================================
# 3. SECCIÓN DE REDES
# ==========================================
def lista_redes(request):
    redes = Red.objects.all()
    return render(request, 'inventario_equipos/red_list.html', {'redes': redes})

def crear_red(request):
    if request.method == 'POST':
        form = RedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Red registrada exitosamente.')
            return redirect('lista_redes')
        else:
            messages.error(request, 'Error al registrar la red.')
    else:
        form = RedForm()
    return render(request, 'inventario_equipos/red_form.html', {'form': form})

def editar_red(request, pk):
    red = get_object_or_404(Red, pk=pk)
    if request.method == 'POST':
        form = RedForm(request.POST, instance=red)
        if form.is_valid():
            form.save()
            messages.success(request, 'Red actualizada.')
            return redirect('lista_redes')
        else:
            messages.error(request, 'Error al actualizar la red.')
    else:
        form = RedForm(instance=red)
    return render(request, 'inventario_equipos/red_form.html', {'form': form})

def eliminar_red(request, pk):
    red = get_object_or_404(Red, pk=pk)
    if request.method == 'POST':
        red.delete()
        messages.success(request, 'Red eliminada.')
        return redirect('lista_redes')
    return render(request, 'inventario_equipos/red_confirm_delete.html', {'red': red})