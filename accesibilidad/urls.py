from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_accesibilidad, name='menu_accesibilidad'),
    path('nueva/', views.realizar_encuesta, name='realizar_encuesta'),
    path('resultados/', views.resultados_accesibilidad, name='resultados_accesibilidad'),
]