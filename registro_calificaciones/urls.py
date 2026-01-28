from django.urls import path
from . import views

app_name = 'registro_calificaciones'

urlpatterns = [
    # --- DASHBOARD E INICIO ---
    path('', views.dashboard_calificaciones, name='inicio'),
    path('dashboard/', views.dashboard_calificaciones, name='dashboard_calificaciones'),

    # --- ESTUDIANTES ---
    path('estudiantes/', views.lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/crear/', views.crear_estudiante, name='crear_estudiante'),
    path('estudiantes/<int:pk>/editar/', views.editar_estudiante, name='editar_estudiante'),
    path('estudiantes/<int:pk>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),
    path('estudiantes/<int:pk>/', views.detalle_estudiante, name='detalle_estudiante'),
    
    # Acciones sobre estudiantes
    path('estudiantes/<int:estudiante_id>/matricular/', views.matricular_estudiante_curso, name='matricular_estudiante_curso'),
    path('estudiantes/<int:estudiante_id>/calificar/', views.registrar_calificacion_estudiante, name='registrar_calificacion_estudiante'),

    # --- MATRÍCULAS ---
    path('matriculas/', views.lista_matriculas, name='lista_matriculas'),
    path('matriculas/crear/', views.crear_matricula, name='crear_matricula'),
    path('matriculas/<int:pk>/editar/', views.editar_matricula, name='editar_matricula'),
    path('matriculas/<int:pk>/eliminar/', views.eliminar_matricula, name='eliminar_matricula'),
    
    # --- PROFESORES ---
    path('profesores/', views.lista_profesores, name='lista_profesores'),
    path('profesores/crear/', views.crear_profesor, name='crear_profesor'),
    path('profesores/<int:pk>/editar/', views.editar_profesor, name='editar_profesor'),
    path('profesores/<int:pk>/eliminar/', views.eliminar_profesor, name='eliminar_profesor'),
    
    # --- CURSOS ---
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/crear/', views.crear_curso, name='crear_curso'),
    path('cursos/<int:pk>/editar/', views.editar_curso, name='editar_curso'),
    path('cursos/<int:pk>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    
    # Ver lista de alumnos de un curso específico (El "Ojito")
    path('cursos/<int:curso_id>/estudiantes/', views.ver_estudiantes_curso, name='ver_estudiantes_curso'),
    
    # Gestión de Materias (Asignaturas)
    path('cursos/<int:curso_id>/asignaturas/', views.gestionar_asignaturas, name='gestionar_asignaturas'),
    
    # Sábana de notas 70/30 (Gestión)
    path('cursos/<int:curso_id>/notas/', views.gestionar_notas_curso, name='gestionar_notas_curso'),
    
    # --- CALIFICACIONES ---
    path('calificaciones/', views.lista_calificaciones, name='lista_calificaciones'),
    path('calificaciones/registro-multiple/', views.registro_multiple_calificaciones, name='registro_multiple_calificaciones'),
    path('calificaciones/<int:pk>/editar/', views.editar_calificacion, name='editar_calificacion'),
    # NUEVA LÍNEA AGREGADA:
    path('calificaciones/<int:pk>/eliminar/', views.eliminar_calificacion, name='eliminar_calificacion'),
    
    # --- IMPRESIÓN ---
    # Impresión individual (Boleta)
    path('matricula/<int:matricula_id>/imprimir/', views.imprimir_boleta, name='imprimir_boleta'),
    
    # Impresión de Sábana de Notas por materia (Reporte Docente)
    path('imprimir-sabana/<int:curso_id>/<int:asignatura_id>/', views.imprimir_sabana_asignatura, name='imprimir_sabana_asignatura'),

    # --- API (AJAX) ---
    path('api/estudiantes-curso/<int:curso_id>/', views.obtener_estudiantes_curso, name='obtener_estudiantes_curso'),
    
    # --- REPORTES ---
    path('reportes/generar/', views.generar_reporte_calificaciones, name='generar_reporte_calificaciones'),
    path('reportes/', views.lista_reportes_calificaciones, name='lista_reportes_calificaciones'),
]