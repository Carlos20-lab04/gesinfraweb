from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import EncuestaAccesibilidad
from .forms import EncuestaAccesibilidadForm

# --- VISTA PARA RESPONDER LA ENCUESTA ---
@login_required
def responder_encuesta(request):
    if request.method == 'POST':
        form = EncuestaAccesibilidadForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            # Si quieres guardar el nombre del usuario logueado automáticamente:
            # encuesta.nombre_encuestado = request.user.username 
            encuesta.save()
            messages.success(request, '¡Gracias! Tu encuesta de accesibilidad ha sido registrada.')
            return redirect('resultados_accesibilidad')
    else:
        form = EncuestaAccesibilidadForm()
    
    return render(request, 'accesibilidad/encuesta_form.html', {'form': form})

# --- VISTA PARA VER LOS RESULTADOS (GRÁFICOS) ---
@login_required
def resultados_accesibilidad(request):
    # Lista exacta de los campos que definimos en models.py
    campos = [
        'q1_interfaz', 
        'q2_capacitacion', 
        'q3_compatibilidad', 
        'q4_soporte',
        'q5_instalaciones', 
        'q6_apoyo', 
        'q7_recursos_tec', 
        'q8_metodologias',
        'q9_materiales', 
        'q10_adaptaciones', 
        'q11_barreras', 
        'q12_politicas',
        'q13_capacitacion_inst', 
        'q14_conocimiento_bap'
    ]
    
    datos_graficos = []

    for campo in campos:
        # 1. Obtenemos la pregunta completa (verbose_name)
        campo_obj = EncuestaAccesibilidad._meta.get_field(campo)
        pregunta_texto = campo_obj.verbose_name
        
        # 2. Obtenemos el diccionario de opciones para traducir "si" -> "Sí"
        opciones_dict = dict(campo_obj.choices)
        
        # 3. Contamos las respuestas en la base de datos
        # Esto agrupa por respuesta y las cuenta. Ej: [{'q1_interfaz': 'si', 'total': 5}, ...]
        conteo = EncuestaAccesibilidad.objects.values(campo).annotate(total=Count(campo)).order_by()
        
        labels = []
        data = []
        
        for item in conteo:
            valor_bd = item[campo]  # El valor guardado (ej: "obstaculo")
            if valor_bd: # Evitar vacíos
                # Traducimos el valor BD al texto legible usando el diccionario
                texto_legible = opciones_dict.get(valor_bd, valor_bd)
                
                labels.append(texto_legible)
                data.append(item['total'])
        
        # Guardamos todo el paquete de datos para este gráfico
        datos_graficos.append({
            'id': campo,
            'titulo': pregunta_texto,
            'labels': labels,
            'data': data
        })

    return render(request, 'accesibilidad/resultados.html', {'datos_graficos': datos_graficos})