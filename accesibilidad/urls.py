from django.urls import path
from . import views

urlpatterns = [
    # 1. Cuando entren a /accesibilidad/, los mandamos directo a RESPONDER la encuesta
    # Usamos name='menu_accesibilidad' para no romper enlaces antiguos en tu menú
    path('', views.responder_encuesta, name='menu_accesibilidad'),

    # 2. Ruta explícita para responder
    path('responder/', views.responder_encuesta, name='responder_encuesta'),

    # 3. Ruta para ver los resultados (gráficos)
    path('resultados/', views.resultados_accesibilidad, name='resultados_accesibilidad'),
]