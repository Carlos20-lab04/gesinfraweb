from django.urls import path
from . import views

# COMENTA O ELIMINA ESTA LÍNEA para evitar errores de namespace:
# app_name = 'inventario_equipos'

urlpatterns = [
    # Menú Principal de Tecnología
    path('menu/', views.menu_inventario, name='menu_principal'),

    # Equipos
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('equipos/crear/', views.crear_equipo, name='crear_equipo'),
    path('equipos/<int:pk>/editar/', views.editar_equipo, name='editar_equipo'),
    path('equipos/<int:pk>/eliminar/', views.eliminar_equipo, name='eliminar_equipo'),
    
    # Mantenimientos
    path('mantenimientos/', views.lista_mantenimientos, name='lista_mantenimientos'),
    path('mantenimientos/crear/', views.crear_mantenimiento, name='crear_mantenimiento'),
    path('mantenimientos/<int:pk>/editar/', views.editar_mantenimiento, name='editar_mantenimiento'),
    path('mantenimientos/<int:pk>/eliminar/', views.eliminar_mantenimiento, name='eliminar_mantenimiento'),
    
    # Redes
    path('redes/', views.lista_redes, name='lista_redes'),
    path('redes/crear/', views.crear_red, name='crear_red'),
    path('redes/<int:pk>/editar/', views.editar_red, name='editar_red'),
    path('redes/<int:pk>/eliminar/', views.eliminar_red, name='eliminar_red'),
]