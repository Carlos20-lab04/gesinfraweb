from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
import json
from datetime import datetime

# Importamos todos los modelos
from .models import Estudiante, Profesor, Curso, Calificacion, Matricula, ReporteCalificaciones, Asignatura
from .forms import (
    EstudianteForm, ProfesorForm, CursoForm, CalificacionForm, 
    MatriculaForm, ReporteCalificacionesForm, FiltroCalificacionesForm,
    BusquedaEstudianteForm, RegistroMultipleCalificacionesForm, AsignaturaForm,
    ConfiguracionPromedioForm
)

# ============================================
# 1. GESTIÓN DE NOTAS (SÁBANA DE NOTAS Y BOLETA)
# ============================================

@login_required
def gestionar_notas_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    asignaturas = curso.asignaturas.all()
    
    asignatura_id = request.GET.get('asignatura')
    asignatura_seleccionada = None
    tabla_calificaciones = []
    nombres_actividades = [] 
    
    # Valores por defecto para el cálculo del 30%
    usar_examen = True
    usar_proyecto = True
    form_conf = ConfiguracionPromedioForm(initial={'incluir_examen': True, 'incluir_proyecto': True})

    # Si el profesor envió la configuración (casillas marcadas/desmarcadas)
    if request.method == 'POST' and 'conf_promedio' in request.POST:
        form_conf = ConfiguracionPromedioForm(request.POST)
        if form_conf.is_valid():
            usar_examen = form_conf.cleaned_data['incluir_examen']
            usar_proyecto = form_conf.cleaned_data['incluir_proyecto']
            # Mantenemos la asignatura seleccionada en el POST para no perder la vista
            asignatura_id = request.POST.get('asignatura_id_hidden')

    if asignatura_id:
        asignatura_seleccionada = get_object_or_404(Asignatura, pk=asignatura_id)
        
        # Obtener nombres de actividades únicos para las columnas (T1)
        nombres_actividades = Calificacion.objects.filter(
            asignatura=asignatura_seleccionada,
            matricula__curso=curso,
            tipo_evaluacion='actividad',
            periodo_academico='T1' 
        ).values_list('nombre_actividad', flat=True).distinct().order_by('id')

        matriculas = Matricula.objects.filter(curso=curso, estado='activo').select_related('estudiante', 'estudiante__usuario').order_by('estudiante__usuario__last_name')

        for matricula in matriculas:
            notas_base = Calificacion.objects.filter(matricula=matricula, asignatura=asignatura_seleccionada, periodo_academico='T1')

            # --- 1. Cálculo del 70% (Actividades) ---
            prom_actividades = notas_base.filter(tipo_evaluacion='actividad').aggregate(prom=Avg('nota'))['prom'] or 0
            ponderado_70 = float(prom_actividades) * 0.70
            
            # --- 2. Obtención de notas de evaluación ---
            nota_proy_obj = notas_base.filter(tipo_evaluacion='proyecto').first()
            nota_exam_obj = notas_base.filter(tipo_evaluacion='examen').first()
            
            val_proy = float(nota_proy_obj.nota) if nota_proy_obj else 0
            val_exam = float(nota_exam_obj.nota) if nota_exam_obj else 0
            
            # --- 3. Cálculo del 30% (LÓGICA CONDICIONAL NUEVA) ---
            ponderado_30 = 0
            
            if usar_examen and usar_proyecto:
                # Caso Estándar: Examen 20% + Proyecto 10%
                ponderado_30 = (val_exam * 0.20) + (val_proy * 0.10)
            elif usar_examen and not usar_proyecto:
                # Solo Examen: Vale el 30%
                ponderado_30 = val_exam * 0.30
            elif usar_proyecto and not usar_examen:
                # Solo Proyecto: Vale el 30%
                ponderado_30 = val_proy * 0.30
            
            # Nota Final
            nota_final = ponderado_70 + ponderado_30
            
            # --- Notas individuales para la tabla ---
            notas_individuales = []
            for nombre_col in nombres_actividades:
                nota_obj = notas_base.filter(
                    tipo_evaluacion='actividad',
                    nombre_actividad=nombre_col
                ).first()
                notas_individuales.append(nota_obj.nota if nota_obj else "-")

            tabla_calificaciones.append({
                'estudiante': matricula.estudiante,
                'matricula_id': matricula.id,
                'notas_individuales': notas_individuales,
                'prom_actividades': round(prom_actividades, 2),
                'ponderado_70': round(ponderado_70, 2),
                'valor_proyecto': val_proy,
                'valor_examen': val_exam,
                'ponderado_30': round(ponderado_30, 2),
                'nota_final': round(nota_final, 2),
                'aprobado': nota_final >= 7
            })

    return render(request, 'registro_calificaciones/gestion_notas.html', {
        'curso': curso,
        'asignaturas': asignaturas,
        'asignatura_seleccionada': asignatura_seleccionada,
        'tabla_calificaciones': tabla_calificaciones,
        'nombres_actividades': nombres_actividades,
        'form_conf': form_conf, 
    })

@login_required
def imprimir_boleta(request, matricula_id):
    matricula = get_object_or_404(Matricula, pk=matricula_id)
    curso = matricula.curso
    asignaturas = curso.asignaturas.all()
    
    boleta_items = []
    promedio_general_suma = 0
    total_materias = 0

    for asignatura in asignaturas:
        notas = Calificacion.objects.filter(matricula=matricula, asignatura=asignatura)
        
        # 70%
        prom_act = notas.filter(tipo_evaluacion='actividad').aggregate(prom=Avg('nota'))['prom'] or 0
        p70 = float(prom_act) * 0.70
        
        # 30% (Por defecto estándar: 20% Examen + 10% Proyecto para impresión)
        n_proy = notas.filter(tipo_evaluacion='proyecto').first()
        n_exam = notas.filter(tipo_evaluacion='examen').first()
        v_proy = float(n_proy.nota) if n_proy else 0
        v_exam = float(n_exam.nota) if n_exam else 0
        
        # Cálculo corregido: 20% y 10%
        p30 = (v_exam * 0.20) + (v_proy * 0.10)
        
        nota_final = p70 + p30
        
        boleta_items.append({
            'asignatura': asignatura.nombre,
            'profesor': asignatura.profesor if asignatura.profesor else curso.profesor,
            'prom_actividades': round(prom_act, 2),
            'nota_proyecto': v_proy,
            'nota_examen': v_exam,
            'nota_final': round(nota_final, 2),
            'estado': 'Aprobado' if nota_final >= 7 else 'Reprobado'
        })
        promedio_general_suma += nota_final
        total_materias += 1
    
    promedio_general = promedio_general_suma / total_materias if total_materias > 0 else 0

    context = {
        'estudiante': matricula.estudiante,
        'curso': curso,
        'matricula': matricula,
        'boleta_items': boleta_items,
        'promedio_general': round(promedio_general, 2),
        'fecha': datetime.now(), 
    }
    return render(request, 'registro_calificaciones/boleta_impresion.html', context)

@login_required
def imprimir_sabana_asignatura(request, curso_id, asignatura_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    asignatura = get_object_or_404(Asignatura, pk=asignatura_id)
    
    nombres_actividades = Calificacion.objects.filter(
        asignatura=asignatura,
        matricula__curso=curso,
        tipo_evaluacion='actividad',
        periodo_academico='T1'
    ).values_list('nombre_actividad', flat=True).distinct().order_by('id')

    matriculas = Matricula.objects.filter(
        curso=curso, 
        estado='activo'
    ).select_related('estudiante', 'estudiante__usuario').order_by('estudiante__usuario__last_name', 'estudiante__usuario__first_name')

    tabla_calificaciones = []

    for matricula in matriculas:
        notas_base = Calificacion.objects.filter(matricula=matricula, asignatura=asignatura, periodo_academico='T1')

        prom_actividades = notas_base.filter(tipo_evaluacion='actividad').aggregate(prom=Avg('nota'))['prom'] or 0
        ponderado_70 = float(prom_actividades) * 0.70
        
        nota_proy = notas_base.filter(tipo_evaluacion='proyecto').first()
        nota_exam = notas_base.filter(tipo_evaluacion='examen').first()
        
        val_proy = float(nota_proy.nota) if nota_proy else 0
        val_exam = float(nota_exam.nota) if nota_exam else 0
        
        # Lógica por defecto para impresión (20% Examen + 10% Proyecto)
        ponderado_30 = (val_exam * 0.20) + (val_proy * 0.10)
        
        nota_final = ponderado_70 + ponderado_30
        
        notas_individuales = []
        for nombre_col in nombres_actividades:
            nota_obj = notas_base.filter(
                tipo_evaluacion='actividad', 
                nombre_actividad=nombre_col
            ).first()
            notas_individuales.append(nota_obj.nota if nota_obj else "-")
        
        tabla_calificaciones.append({
            'estudiante': matricula.estudiante,
            'notas_individuales': notas_individuales,
            'prom_actividades': round(prom_actividades, 2),
            'ponderado_70': round(ponderado_70, 2),
            'valor_proyecto': val_proy,
            'valor_examen': val_exam,
            'ponderado_30': round(ponderado_30, 2),
            'nota_final': round(nota_final, 2),
            'aprobado': nota_final >= 7
        })

    return render(request, 'registro_calificaciones/imprimir_sabana.html', {
        'curso': curso,
        'asignatura': asignatura,
        'tabla_calificaciones': tabla_calificaciones,
        'nombres_actividades': nombres_actividades,
        'profesor': asignatura.profesor if asignatura.profesor else curso.profesor,
        'fecha_impresion': datetime.now()
    })

# ============================================
# 2. ESTUDIANTES Y MATRÍCULAS
# ============================================

@login_required
def lista_estudiantes(request):
    form_busqueda = BusquedaEstudianteForm(request.GET or None)
    estudiantes = Estudiante.objects.all().select_related('usuario').order_by('-id')

    if form_busqueda.is_valid():
        termino = form_busqueda.cleaned_data.get('termino_busqueda')
        if termino:
            estudiantes = estudiantes.filter(
                Q(usuario__first_name__icontains=termino) |
                Q(usuario__last_name__icontains=termino) |
                Q(cedula__icontains=termino)
            )

    paginator = Paginator(estudiantes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'registro_calificaciones/estudiante_list.html', {
        'page_obj': page_obj,
        'form_busqueda': form_busqueda
    })

@login_required
def crear_estudiante(request):
    curso_retorno_id = request.GET.get('return_curso_id')

    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save()
            
            if curso_retorno_id:
                messages.success(request, 'Estudiante creado. Ahora finalice la matrícula.')
                base_url = reverse('registro_calificaciones:crear_matricula')
                return redirect(f'{base_url}?curso_id={curso_retorno_id}&estudiante_id={estudiante.id}')
            
            return redirect('registro_calificaciones:matricular_estudiante_curso', estudiante_id=estudiante.id)
    else:
        form = EstudianteForm()
    
    return render(request, 'registro_calificaciones/estudiante_form.html', {
        'form': form, 
        'titulo': 'Crear Estudiante', 
        'accion': 'crear'
    })

@login_required
def editar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estudiante actualizado.')
            return redirect('registro_calificaciones:detalle_estudiante', pk=pk)
    else:
        form = EstudianteForm(instance=estudiante)
    return render(request, 'registro_calificaciones/estudiante_form.html', {'form': form, 'titulo': 'Editar Estudiante', 'accion': 'editar'})

@login_required
def eliminar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == 'POST':
        estudiante.delete()
        messages.success(request, 'Estudiante eliminado.')
        return redirect('registro_calificaciones:lista_estudiantes')
    return render(request, 'registro_calificaciones/estudiante_confirm_delete.html', {'estudiante': estudiante})

@login_required
def detalle_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    matriculas = Matricula.objects.filter(estudiante=estudiante).select_related('curso')
    calificaciones = Calificacion.objects.filter(matricula__estudiante=estudiante).order_by('-fecha_registro')[:10]

    return render(request, 'registro_calificaciones/estudiante_detail.html', {
        'estudiante': estudiante,
        'matriculas': matriculas,
        'calificaciones': calificaciones
    })

@login_required
def matricular_estudiante_curso(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.estudiante = estudiante
            matricula.save()
            messages.success(request, f'Matriculado en {matricula.curso}')
            return redirect('registro_calificaciones:detalle_estudiante', pk=estudiante_id)
    else:
        form = MatriculaForm(initial={'estudiante': estudiante})
    
    return render(request, 'registro_calificaciones/matricular_estudiante.html', {'form': form, 'estudiante': estudiante})

@login_required
def lista_matriculas(request):
    matriculas = Matricula.objects.all().select_related('estudiante', 'curso')
    paginator = Paginator(matriculas, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'registro_calificaciones/matricula_list.html', {'page_obj': page_obj})

@login_required
def crear_matricula(request):
    initial_data = {}
    
    curso_id_param = request.GET.get('curso_id')
    estudiante_id_param = request.GET.get('estudiante_id') 
    
    if curso_id_param:
        curso_obj = get_object_or_404(Curso, pk=curso_id_param)
        initial_data['curso'] = curso_obj
    
    if estudiante_id_param:
        estudiante_obj = get_object_or_404(Estudiante, pk=estudiante_id_param)
        initial_data['estudiante'] = estudiante_obj

    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save()
            
            if curso_id_param:
                messages.success(request, "Estudiante matriculado con éxito.")
                return redirect('registro_calificaciones:ver_estudiantes_curso', curso_id=curso_id_param)
            
            return redirect('registro_calificaciones:lista_matriculas')
    else:
        form = MatriculaForm(initial=initial_data)

    return render(request, 'registro_calificaciones/matricula_form.html', {
        'form': form, 
        'titulo': 'Registrar Matrícula',
        'curso_id': curso_id_param 
    })

@login_required
def editar_matricula(request, pk):
    matricula = get_object_or_404(Matricula, pk=pk)
    if request.method == 'POST':
        form = MatriculaForm(request.POST, instance=matricula)
        if form.is_valid():
            form.save()
            return redirect('registro_calificaciones:lista_matriculas')
    else:
        form = MatriculaForm(instance=matricula)
    return render(request, 'registro_calificaciones/matricula_form.html', {'form': form, 'titulo': 'Editar Matrícula'})

@login_required
def eliminar_matricula(request, pk):
    matricula = get_object_or_404(Matricula, pk=pk)
    if request.method == 'POST':
        matricula.delete()
        return redirect('registro_calificaciones:lista_matriculas')
    return render(request, 'registro_calificaciones/matricula_confirm_delete.html', {'matricula': matricula})


# ============================================
# 3. CALIFICACIONES (INDIVIDUAL, MÚLTIPLE Y EDICIÓN)
# ============================================

@login_required
def registrar_calificacion_estudiante(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    matricula = Matricula.objects.filter(estudiante=estudiante, estado='activo').first()

    # Capturamos la asignatura de la URL
    asignatura_id_preseleccionada = request.GET.get('asignatura')

    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            if not matricula:
                messages.error(request, "El estudiante no tiene matrícula activa.")
                return redirect('registro_calificaciones:lista_estudiantes')

            if calificacion.asignatura.curso != matricula.curso:
                messages.error(request, "La asignatura seleccionada no corresponde al curso del estudiante.")
                return render(request, 'registro_calificaciones/calificacion_form.html', {'form': form, 'estudiante': estudiante})

            calificacion.matricula = matricula

            try:
                profesor = Profesor.objects.get(usuario=request.user)
                calificacion.profesor = profesor
            except Profesor.DoesNotExist:
                calificacion.profesor = calificacion.asignatura.curso.profesor
            
            calificacion.save()
            messages.success(request, f'Calificación guardada.')
            
            # --- CAMBIO CLAVE: REDIRECCIÓN A LA SÁBANA DE NOTAS ---
            # Obtenemos el ID del curso y de la asignatura para volver exactamente a la tabla
            curso_id = matricula.curso.id
            asignatura_id = calificacion.asignatura.id
            
            base_url = reverse('registro_calificaciones:gestionar_notas_curso', args=[curso_id])
            return redirect(f"{base_url}?asignatura={asignatura_id}")

    else:
        initial_data = {}
        if asignatura_id_preseleccionada:
            initial_data['asignatura'] = asignatura_id_preseleccionada

        form = CalificacionForm(initial=initial_data)
        if matricula:
            form.fields['asignatura'].queryset = Asignatura.objects.filter(curso=matricula.curso)
    
    resumen_trimestres = {'T1': [], 'T2': [], 'T3': []}
    if matricula:
        asignaturas_con_notas = Asignatura.objects.filter(calificaciones__matricula=matricula).distinct()
        for codigo_tri, nombre_tri in [('T1', 'Trimestre 1'), ('T2', 'Trimestre 2'), ('T3', 'Trimestre 3')]:
            datos_por_asignatura = []
            for asignatura in asignaturas_con_notas:
                notas = Calificacion.objects.filter(matricula=matricula, asignatura=asignatura, periodo_academico=codigo_tri)
                if notas.exists():
                    prom_act = notas.filter(tipo_evaluacion='actividad').aggregate(prom=Avg('nota'))['prom'] or 0
                    
                    # Cálculo estándar por defecto para la vista individual
                    n_proy = notas.filter(tipo_evaluacion='proyecto').first()
                    n_exam = notas.filter(tipo_evaluacion='examen').first()
                    v_proy = float(n_proy.nota) if n_proy else 0
                    v_exam = float(n_exam.nota) if n_exam else 0
                    
                    # 20% examen + 10% proyecto
                    prom_eval = (v_exam * 0.20) + (v_proy * 0.10)
                    
                    nota_final = (float(prom_act) * 0.70) + prom_eval
                    
                    datos_por_asignatura.append({
                        'asignatura': asignatura,
                        'notas': notas,
                        'promedio_final': round(nota_final, 2)
                    })
            resumen_trimestres[codigo_tri] = datos_por_asignatura

    return render(request, 'registro_calificaciones/calificacion_form.html', {
        'form': form, 
        'estudiante': estudiante,
        'matricula': matricula, # Necesario para el botón volver en HTML
        'resumen_trimestres': resumen_trimestres,
        'asignatura_preseleccionada': int(asignatura_id_preseleccionada) if asignatura_id_preseleccionada else None
    })

@login_required
def editar_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    estudiante = calificacion.matricula.estudiante
    matricula = calificacion.matricula # Necesario para contexto

    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            calificacion_guardada = form.save()
            messages.success(request, "Calificación actualizada correctamente.")
            
            # --- CAMBIO CLAVE: REDIRECCIÓN A LA SÁBANA DE NOTAS ---
            curso_id = calificacion_guardada.matricula.curso.id
            asignatura_id = calificacion_guardada.asignatura.id
            
            base_url = reverse('registro_calificaciones:gestionar_notas_curso', args=[curso_id])
            return redirect(f"{base_url}?asignatura={asignatura_id}")
    else:
        form = CalificacionForm(instance=calificacion)
        form.fields['asignatura'].queryset = Asignatura.objects.filter(curso=calificacion.matricula.curso)
    
    return render(request, 'registro_calificaciones/calificacion_form.html', {
        'form': form,
        'estudiante': estudiante,
        'matricula': matricula, # Pasamos la matrícula para el botón volver
        'editando': True,
        'asignatura_preseleccionada': calificacion.asignatura.id 
    })

@login_required
def eliminar_calificacion(request, pk):
    """
    Vista para eliminar una calificación y retornar a la sábana de notas.
    """
    calificacion = get_object_or_404(Calificacion, pk=pk)
    
    # Guardamos los IDs antes de borrar para saber a dónde volver
    curso_id = calificacion.matricula.curso.id
    asignatura_id = calificacion.asignatura.id
    
    # Eliminamos
    calificacion.delete()
    messages.success(request, "Calificación eliminada correctamente.")
    
    # Redirigimos a la Sábana de Notas
    base_url = reverse('registro_calificaciones:gestionar_notas_curso', args=[curso_id])
    return redirect(f"{base_url}?asignatura={asignatura_id}")

@login_required
def registro_multiple_calificaciones(request):
    if request.method == 'POST':
        form = RegistroMultipleCalificacionesForm(request.POST)
        if form.is_valid():
            curso = form.cleaned_data['curso']
            asignatura = get_object_or_404(Asignatura, pk=request.POST.get('asignatura'))
            tipo_eval = form.cleaned_data['tipo_evaluacion']
            periodo = form.cleaned_data['periodo_academico']
            
            data_dict = json.loads(request.POST.get('calificaciones', '{}'))
            profesor = Profesor.objects.filter(usuario=request.user).first() or curso.profesor

            for mid, info in data_dict.items():
                if info.get('nota'):
                    Calificacion.objects.update_or_create(
                        matricula_id=mid, asignatura=asignatura, tipo_evaluacion=tipo_eval, periodo_academico=periodo,
                        defaults={'nota': float(info['nota']), 'profesor': profesor, 'nombre_actividad': 'Carga Masiva'}
                    )
            messages.success(request, "Notas registradas.")
            return redirect('registro_calificaciones:gestionar_notas_curso', curso_id=curso.id)
    else:
        form = RegistroMultipleCalificacionesForm()
    return render(request, 'registro_calificaciones/registro_multiple_form.html', {'form': form})

@login_required
def lista_calificaciones(request):
    calificaciones = Calificacion.objects.all().order_by('-fecha_registro')
    paginator = Paginator(calificaciones, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'registro_calificaciones/calificacion_list.html', {'page_obj': page_obj})

# ============================================
# 4. PROFESORES, CURSOS Y ASIGNATURAS
# ============================================

@login_required
def lista_profesores(request):
    profesores = Profesor.objects.all()
    return render(request, 'registro_calificaciones/profesor_list.html', {'profesores': profesores})

@login_required
def crear_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_calificaciones:lista_profesores')
    else:
        form = ProfesorForm()
    return render(request, 'registro_calificaciones/profesor_form.html', {'form': form, 'titulo': 'Crear Profesor'})

@login_required
def editar_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('registro_calificaciones:lista_profesores')
    else:
        form = ProfesorForm(instance=profesor)
    return render(request, 'registro_calificaciones/profesor_form.html', {'form': form, 'titulo': 'Editar Profesor'})

@login_required
def eliminar_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    if request.method == 'POST':
        profesor.delete()
        return redirect('registro_calificaciones:lista_profesores')
    return render(request, 'registro_calificaciones/profesor_confirm_delete.html', {'profesor': profesor})

@login_required
def lista_cursos(request):
    cursos = Curso.objects.annotate(
        total_estudiantes=Count('matriculas', filter=Q(matriculas__estado='activo'))
    ).order_by('nombre')
    return render(request, 'registro_calificaciones/curso_list.html', {'cursos': cursos})

@login_required
def ver_estudiantes_curso(request, curso_id):
    """Muestra la lista de estudiantes matriculados en un curso específico"""
    curso = get_object_or_404(Curso, pk=curso_id)
    matriculas = Matricula.objects.filter(curso=curso, estado='activo').select_related('estudiante', 'estudiante__usuario')
    return render(request, 'registro_calificaciones/estudiantes_por_curso.html', {
        'curso': curso,
        'matriculas': matriculas
    })

@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_calificaciones:lista_cursos')
    else:
        form = CursoForm()
    return render(request, 'registro_calificaciones/curso_form.html', {'form': form})

@login_required
def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('registro_calificaciones:lista_cursos')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'registro_calificaciones/curso_form.html', {'form': form})

@login_required
def eliminar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        return redirect('registro_calificaciones:lista_cursos')
    return render(request, 'registro_calificaciones/curso_confirm_delete.html', {'curso': curso})

@login_required
def gestionar_asignaturas(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    asignaturas = curso.asignaturas.all() 
    
    if request.method == 'POST':
        if 'eliminar_asignatura' in request.POST:
            asignatura_id = request.POST.get('asignatura_id')
            get_object_or_404(Asignatura, id=asignatura_id, curso=curso).delete()
            messages.success(request, "Materia eliminada.")
            return redirect('registro_calificaciones:gestionar_asignaturas', curso_id=curso.id)

        form = AsignaturaForm(request.POST)
        if form.is_valid():
            nueva_asignatura = form.save(commit=False)
            nueva_asignatura.curso = curso
            nueva_asignatura.save()
            messages.success(request, "Materia agregada.")
            return redirect('registro_calificaciones:gestionar_asignaturas', curso_id=curso.id)
    else:
        form = AsignaturaForm()

    return render(request, 'registro_calificaciones/asignaturas_curso.html', {
        'curso': curso, 'asignaturas': asignaturas, 'form': form
    })

# ============================================
# 5. DASHBOARD, API Y REPORTES
# ============================================

@login_required
def dashboard_calificaciones(request):
    return render(request, 'home.html', {
        'total_estudiantes': Estudiante.objects.count(), 
        'total_cursos': Curso.objects.count(),
        'total_asignaturas': Asignatura.objects.count()
    })

@login_required
def obtener_estudiantes_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    asignaturas = list(curso.asignaturas.all().values('id', 'nombre'))
    estudiantes = [{'id': m.estudiante.id, 'nombre': str(m.estudiante)} for m in Matricula.objects.filter(curso=curso, estado='activo')]
    return JsonResponse({'estudiantes': estudiantes, 'asignaturas': asignaturas})

@login_required
def lista_reportes_calificaciones(request):
    reportes = ReporteCalificaciones.objects.all().order_by('-fecha_generacion')
    return render(request, 'registro_calificaciones/reporte_list.html', {'reportes': reportes})

@login_required
def generar_reporte_calificaciones(request):
    if request.method == 'POST':
        form = ReporteCalificacionesForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.generado_por = request.user
            reporte.save()
            return redirect('registro_calificaciones:lista_reportes_calificaciones')
    else:
        form = ReporteCalificacionesForm()
    return render(request, 'registro_calificaciones/generar_reporte.html', {'form': form})