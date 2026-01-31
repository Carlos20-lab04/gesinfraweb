from django.shortcuts import render, redirect
from django.contrib import messages
from collections import Counter
from .models import EncuestaAccesibilidad
from .forms import EncuestaAccesibilidadForm

def responder_encuesta(request):
    if request.method == 'POST':
        form = EncuestaAccesibilidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Gracias! Tu encuesta ha sido guardada exitosamente.')
            return redirect('resultados_accesibilidad')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = EncuestaAccesibilidadForm()

    return render(request, 'accesibilidad/encuesta_form.html', {'form': form})

def resultados_accesibilidad(request):
    # 1. Definimos la configuración de qué campos queremos graficar y sus títulos
    # El 'campo' debe ser IGUAL al nombre en models.py
    configuracion_preguntas = [
        {'campo': 'q1_interfaz', 'titulo': '1. ¿Considera que la interfaz (organización visual, menús y botones de la pantalla) de la plataforma educativa facilita la localización de las herramientas necesarias para sus actividades?'},
        {'campo': 'q2_capacitacion', 'titulo': '2. ¿De qué manera la ausencia de capacitación sobre el uso de la tecnología, ha afectado su desempeño en la plataforma institucional?'},
        {'campo': 'q3_compatibilidad', 'titulo': '3. ¿Cuál es el nivel de compatibilidad (la capacidad de funcionamiento conjunto) entre sus dispositivos personales y los requisitos técnicos de la plataforma?'},
        {'campo': 'q4_soporte', 'titulo': '4. ¿Ante una falla técnica o un bloqueo de acceso, ¿identifica usted los canales de soporte técnico (el servicio de asistencia para resolver problemas con la tecnología) disponibles?'},
        {'campo': 'q5_instalaciones', 'titulo': '5. ¿Considera que las instalaciones físicas de la institución (entrada, pasillos, aulas) permiten el desplazamiento autónomo y adecuado de personas con discapacidad física?'},
        {'campo': 'q6_apoyo', 'titulo': '6. ¿Cuenta la institución con elementos de apoyo como rampas, ascensores, baños accesibles y señalética inclusiva (letreros claros o en braille) en buen estado)'},
        {'campo': 'q7_recursos_tec', 'titulo': '7. Los recursos tecnológicos (laboratorios, computadoras, plataformas digitales) son accesibles para todos los estudiantes.'},
        {'campo': 'q8_metodologias', 'titulo': '8. ¿Los docentes aplican metodologías inclusivas en el proceso de enseñanza-aprendizaje.?'},
        {'campo': 'q9_materiales', 'titulo': '9. ¿Considera que los contenidos y materiales del módulo están diseñados tomando en cuenta las diversas necesidades educativas (visuales, auditivas o cognitivas) de todos los estudiantes?'},
        {'campo': 'q10_adaptaciones', 'titulo': '10. Se utilizan adaptaciones curriculares o materiales accesibles (audiovisuales, digitales, adaptados).'},
        {'campo': 'q11_barreras', 'titulo': '11. ¿Qué barreras pedagógicas identifica con mayor frecuencia?'},
        {'campo': 'q12_politicas', 'titulo': '12. La institución cuenta con políticas claras sobre inclusión y accesibilidad educativa.'},
        {'campo': 'q13_capacitacion_inst', 'titulo': '13. ¿Ha existido un proceso de capacitación por parte de la institución para que los docentes sepan cómo aplicar la accesibilidad y la inclusión en sus clases?'},
        {'campo': 'q14_conocimiento_bap', 'titulo': '14. ¿Existe un conocimiento institucional claro por parte de directivos y personal, sobre cómo identificar y eliminar las Barreras para el Aprendizaje y la Participación (BAP)?'}
    ]

    datos_graficos = []

    # 2. Recorremos cada pregunta configurada arriba
    for config in configuracion_preguntas:
        campo = config['campo']
        titulo = config['titulo']

        # Obtenemos TODAS las respuestas de la base de datos para esa columna específica
        # values_list devuelve una lista simple: ['Si', 'No', 'Si', 'Tal vez'...]
        respuestas = EncuestaAccesibilidad.objects.values_list(campo, flat=True)

        # Si hay respuestas, las contamos
        if respuestas:
            # Counter crea un diccionario: {'Si': 5, 'No': 2, ...}
            conteo = Counter(respuestas)
            
            # Separamos las etiquetas (keys) y los datos (values) para Chart.js
            labels = list(conteo.keys())
            data = list(conteo.values())
        else:
            labels = []
            data = []

        # Agregamos el objeto a la lista final
        datos_graficos.append({
            'id': campo,       # Usamos el nombre del campo como ID único
            'titulo': titulo,
            'labels': labels,
            'data': data
        })

    return render(request, 'accesibilidad/resultados.html', {
        'datos_graficos': datos_graficos
    })