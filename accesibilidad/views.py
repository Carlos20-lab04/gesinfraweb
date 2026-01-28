from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EncuestaAccesibilidad
from .forms import EncuestaForm
from django.db.models import Count
import json

def menu_accesibilidad(request):
    return render(request, 'accesibilidad/menu_accesibilidad.html')

def realizar_encuesta(request):
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Encuesta guardada correctamente.')
            return redirect('menu_accesibilidad')
        else:
            messages.error(request, 'Error en el formulario.')
    else:
        form = EncuestaForm()
    return render(request, 'accesibilidad/encuesta_form.html', {'form': form})

def resultados_accesibilidad(request):
    encuestas = EncuestaAccesibilidad.objects.all().order_by('-fecha')

    def obtener_datos(campo):
        conteo = EncuestaAccesibilidad.objects.values(campo).annotate(total=Count(campo))
        labels = [item[campo] for item in conteo if item[campo]]
        data = [item['total'] for item in conteo if item[campo]]
        # Etiquetas legibles (opcional, convierte 'si' en 'Si' visualmente en JS)
        return labels, data

    l_interfaz, d_interfaz = obtener_datos('interfaz_facilita')
    l_apoyo, d_apoyo = obtener_datos('elementos_apoyo')
    l_barreras, d_barreras = obtener_datos('barrera_frecuente')
    l_politicas, d_politicas = obtener_datos('politicas_claras')

    context = {
        'encuestas': encuestas,
        'labels_interfaz': l_interfaz, 'data_interfaz': d_interfaz,
        'labels_apoyo': l_apoyo, 'data_apoyo': d_apoyo,
        'labels_barreras': l_barreras, 'data_barreras': d_barreras,
        'labels_politicas': l_politicas, 'data_politicas': d_politicas,
    }
    return render(request, 'accesibilidad/resultados.html', context)