from django.contrib import admin
from .models import Estudiante, Profesor, Curso, Matricula, Calificacion, ReporteCalificaciones, Asignatura

# Registro de modelos en el admin

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    # --- CORREGIDO: Se eliminó 'codigo_estudiante' ---
    list_display = ('usuario', 'cedula', 'año_lectivo', 'telefono')
    list_filter = ('año_lectivo',)
    # --- CORREGIDO: Se eliminó 'codigo_estudiante' de la búsqueda ---
    search_fields = ('usuario__first_name', 'usuario__last_name', 'cedula')
    ordering = ('usuario__last_name', 'usuario__first_name')

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'codigo_profesor', 'especialidad', 'telefono')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'codigo_profesor', 'especialidad')
    ordering = ('usuario__last_name', 'usuario__first_name')

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo_curso', 'nombre', 'creditos', 'año_lectivo', 'profesor')
    list_filter = ('año_lectivo', 'profesor')
    search_fields = ('codigo_curso', 'nombre', 'año_lectivo')
    ordering = ('año_lectivo', 'nombre')

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso') 
    list_filter = ('curso',)
    search_fields = ('nombre', 'curso__nombre')

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    # Agregué 'numero_lista' al principio para que veas el orden
    list_display = ('numero_lista', 'estudiante', 'curso', 'fecha_matricula', 'estado')
    list_filter = ('estado', 'curso', 'fecha_matricula')
    search_fields = ('estudiante__usuario__first_name', 'estudiante__usuario__last_name', 'curso__nombre')
    # Ordenar primero por curso y luego por numero de lista
    ordering = ('curso', 'numero_lista')

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'get_asignatura', 'tipo_evaluacion', 'nota', 'periodo_academico')
    list_filter = ('tipo_evaluacion', 'periodo_academico', 'profesor')
    search_fields = ('matricula__estudiante__usuario__first_name', 
                     'matricula__estudiante__usuario__last_name',
                     'matricula__curso__nombre')
    ordering = ('-fecha_registro',)
    
    def get_asignatura(self, obj):
        return obj.asignatura.nombre if obj.asignatura else "Sin Asignatura"
    get_asignatura.short_description = 'Asignatura'

@admin.register(ReporteCalificaciones)
class ReporteCalificacionesAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_reporte', 'fecha_generacion', 'generado_por')
    list_filter = ('tipo_reporte', 'fecha_generacion')
    search_fields = ('titulo', 'generado_por__username')
    ordering = ('-fecha_generacion',)