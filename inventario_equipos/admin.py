from django.contrib import admin
from .models import Equipo, Mantenimiento, Red

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['codigo_inventario', 'tipo_equipo', 'marca', 'modelo', 'estado', 'ubicacion']
    list_filter = ['tipo_equipo', 'estado', 'ubicacion']
    search_fields = ['codigo_inventario', 'marca', 'modelo', 'numero_serie']

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ['equipo', 'fecha_mantenimiento', 'tipo_mantenimiento', 'estado', 'tecnico']
    list_filter = ['tipo_mantenimiento', 'estado', 'fecha_mantenimiento']
    search_fields = ['equipo__codigo_inventario', 'tecnico']

@admin.register(Red)
class RedAdmin(admin.ModelAdmin):
    list_display = ['nombre_red', 'tipo_red', 'direccion_ip', 'estado', 'ubicacion']
    list_filter = ['tipo_red', 'estado']
    filter_horizontal = ['equipos_conectados']