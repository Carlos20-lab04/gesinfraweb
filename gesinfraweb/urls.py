"""
URL configuration for gesinfraweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for gesinfraweb project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# ✅ AGREGADO 1: Importamos LoginView y login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Apps (Las mantenemos igual)
    path('registro/', include('registro_calificaciones.urls')),
    path('inventario/', include('inventario_equipos.urls')),
    path('accesibilidad/', include('accesibilidad.urls')),
    
    # Autenticación (Lo mantenemos igual)
    path('accounts/', include('django.contrib.auth.urls')),

    # ==========================================
    # 🚨 AQUÍ ESTÁ EL CAMBIO IMPORTANTE
    # ==========================================

    # 1. AHORA LA RAÍZ ES EL LOGIN
    # Cuando entres a 127.0.0.1:8000 verás el Login primero
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),

    # 2. MOVIMOS EL HOME A '/inicio/'
    # Además, le agregamos 'login_required' para que nadie entre escribiendo la URL sin permiso
    path('inicio/', login_required(TemplateView.as_view(template_name='home.html')), name='home'),

]

# Servir archivos media en desarrollo (Esto se mantiene igual)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personalizar admin (Esto se mantiene igual)
admin.site.site_header = "GESINFRA-WEB - Administración"
admin.site.site_title = "Sistema GESINFRA-WEB"
admin.site.index_title = "Panel de Administración"