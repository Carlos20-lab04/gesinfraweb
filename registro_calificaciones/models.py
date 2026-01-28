from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone

class Estudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estudiante')
    
    # --- CAMBIO: Se eliminó codigo_estudiante. La cédula es el identificador único ---
    cedula = models.CharField(max_length=15, unique=True)
    
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    año_lectivo = models.CharField(max_length=20, help_text="Ej: 2025-2026")
    
    def __str__(self):
        # Ahora mostramos la Cédula en lugar del código antiguo
        return f"{self.usuario.first_name} {self.usuario.last_name} ({self.cedula})"

class Profesor(models.Model): 
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profesor')
    codigo_profesor = models.CharField(max_length=20, unique=True)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"Prof. {self.usuario.first_name} {self.usuario.last_name}"

class Curso(models.Model):
    codigo_curso = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200) # Ej: "Decimo EGB - A"
    creditos = models.IntegerField(default=1) 
    año_lectivo = models.CharField(max_length=20, help_text="Ej: 2025-2026")
    descripcion = models.TextField(blank=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, related_name='cursos')
    
    def __str__(self):
        return f"{self.nombre} - {self.año_lectivo}"

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='asignaturas')
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ['nombre', 'curso'] 

    def __str__(self):
        return f"{self.nombre} ({self.curso.nombre})"

class Matricula(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('graduado', 'Graduado'),
        ('retirado', 'Retirado')
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='matriculas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='matriculas')
    fecha_matricula = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    
    # Campo para el número de lista (Ej: 1, 2, 3...)
    numero_lista = models.PositiveIntegerField(
        verbose_name="N° de Lista", 
        null=True, 
        blank=True,
        help_text="Ej: 1, 2, 3... (Se puede repetir en distintos cursos)"
    )
    
    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        unique_together = [
            ['estudiante', 'curso'],       # Un estudiante no puede estar 2 veces en el mismo curso
            ['curso', 'numero_lista']      # En un curso no puede haber dos números repetidos
        ]
        ordering = ['numero_lista', 'estudiante__usuario__last_name']
    
    def __str__(self):
        num = f"#{self.numero_lista}" if self.numero_lista else "S/N"
        return f"{num} - {self.estudiante} en {self.curso}"

class Calificacion(models.Model):
    TIPO_EVALUACION = [
        ('actividad', 'Actividad/Tarea (70%)'),
        ('proyecto', 'Proyecto Final (10%)'),
        ('examen', 'Examen (20%)'),
    ]

    TRIMESTRES = [
        ('T1', 'Trimestre 1'),
        ('T2', 'Trimestre 2'),
        ('T3', 'Trimestre 3'),
    ]

    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='calificaciones')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='calificaciones')
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    
    nombre_actividad = models.CharField(max_length=150, blank=True, null=True, help_text="Ej: Lección pág. 40")
    tipo_evaluacion = models.CharField(max_length=50, choices=TIPO_EVALUACION)
    
    nota = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    
    periodo_academico = models.CharField(max_length=20, choices=TRIMESTRES, default='T1')
    fecha_registro = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Calificaciones'
    
    def __str__(self):
        return f"{self.asignatura.nombre}: {self.nota} ({self.matricula.estudiante.usuario.first_name})"
    
    def obtener_estudiante(self):
        return self.matricula.estudiante
    
    def obtener_curso(self):
        return self.matricula.curso

class ReporteCalificaciones(models.Model):
    titulo = models.CharField(max_length=200)
    tipo_reporte = models.CharField(max_length=50, choices=[
        ('curso', 'Por Curso'),
        ('estudiante', 'Por Estudiante'),
        ('periodo', 'Por Período Académico'),
        ('general', 'General')
    ])
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='reportes_calificaciones/', blank=True, null=True)
    parametros = models.JSONField(default=dict)
    generado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_generacion.strftime('%Y-%m-%d')}"