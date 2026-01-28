from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Estudiante, Profesor, Curso, Calificacion, Matricula, ReporteCalificaciones, Asignatura

# --- FORMULARIOS DE USUARIO ---

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Contraseña")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# --- FORMULARIO DE ESTUDIANTE ---

class EstudianteForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Apellido", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Estudiante
        fields = ['cedula', 'telefono', 'direccion', 'año_lectivo']
        
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'año_lectivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2025-2026'}),
        }
        labels = {
            'año_lectivo': 'Año Lectivo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.usuario:
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['last_name'].initial = self.instance.usuario.last_name
            self.fields['email'].initial = self.instance.usuario.email

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        existing_user = User.objects.filter(username=cedula).first()
        
        if existing_user:
            if hasattr(existing_user, 'estudiante'):
                if self.instance.pk and self.instance.usuario == existing_user:
                    return cedula
                raise ValidationError("Esta cédula ya está registrada y pertenece a un estudiante activo.")
            else:
                pass     
        return cedula

    def clean_año_lectivo(self):
        año_lectivo = self.cleaned_data.get('año_lectivo')
        if año_lectivo and not any(c.isdigit() for c in año_lectivo):
            raise ValidationError("El año lectivo debe contener al menos un número (ej: 2025-2026)")
        return año_lectivo

    def save(self, commit=True):
        with transaction.atomic():
            estudiante = super().save(commit=False)
            
            nombre = self.cleaned_data['first_name']
            apellido = self.cleaned_data['last_name']
            email = self.cleaned_data['email']
            cedula = self.cleaned_data['cedula']

            if estudiante.usuario_id:
                user = estudiante.usuario
                user.first_name = nombre
                user.last_name = apellido
                user.email = email
                if user.username != cedula:
                     user.username = cedula
                user.save()
            else:
                user, created = User.objects.get_or_create(
                    username=cedula,
                    defaults={
                        'email': email,
                        'password': cedula,
                        'first_name': nombre,
                        'last_name': apellido
                    }
                )
                if not created:
                    user.first_name = nombre
                    user.last_name = apellido
                    user.email = email
                    user.save()
                
                estudiante.usuario = user
            
            if commit:
                estudiante.save()
            
            return estudiante

# --- FORMULARIO DE PROFESOR ---

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['codigo_profesor', 'especialidad', 'telefono']
        labels = {
            'codigo_profesor': 'Código del Profesor',
            'especialidad': 'Especialidad',
        }

# --- FORMULARIO DE CURSO ---

class CursoForm(forms.ModelForm):
    OPCIONES_ANIO = [
        ('2023-2024', '2023-2024'),
        ('2024-2025', '2024-2025'),
        ('2025-2026', '2025-2026'),
        ('2026-2027', '2026-2027'),
        ('2027-2028', '2027-2028'),
    ]

    año_lectivo = forms.ChoiceField(
        choices=OPCIONES_ANIO, 
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Año Lectivo"
    )

    class Meta:
        model = Curso
        fields = '__all__'
        
        widgets = {
            'codigo_curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 10-EGB-A'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Decimo EGB - A'}),
            'creditos': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profesor': forms.Select(attrs={'class': 'form-select'}),
        }

# --- FORMULARIO DE ASIGNATURA ---

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'profesor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Matemáticas, Historia'}),
            'profesor': forms.Select(attrs={'class': 'form-select'}),
        }

# --- FORMULARIO DE MATRICULA ---

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['estudiante', 'curso', 'numero_lista', 'estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'estudiante': forms.Select(attrs={'class': 'form-select select2'}),
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'numero_lista': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        estudiante = cleaned_data.get('estudiante')
        curso = cleaned_data.get('curso')
        numero = cleaned_data.get('numero_lista')
        
        # 1. Validación: Estudiante no repetido en el mismo curso
        if estudiante and curso:
            matricula_existente = Matricula.objects.filter(
                estudiante=estudiante, 
                curso=curso
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if matricula_existente.exists():
                self.add_error('estudiante', f"El estudiante {estudiante} ya está matriculado en el curso {curso}.")

        # 2. Validación: Número de lista no repetido en el mismo curso
        if curso and numero:
            numero_existente = Matricula.objects.filter(
                curso=curso,
                numero_lista=numero
            ).exclude(pk=self.instance.pk if self.instance else None)

            if numero_existente.exists():
                self.add_error('numero_lista', f"El número {numero} ya está ocupado en el curso {curso.nombre}.")
                
        return cleaned_data

# --- OTROS FORMULARIOS ---

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['asignatura', 'nombre_actividad', 'tipo_evaluacion', 'nota', 'periodo_academico', 'observaciones']
        
        widgets = {
            'asignatura': forms.Select(attrs={'class': 'form-select'}),
            'nombre_actividad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Tarea Pág 10, Lección Oral...'}),
            'tipo_evaluacion': forms.Select(attrs={'class': 'form-select'}),
            'nota': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '10', 'class': 'form-control'}),
            'periodo_academico': forms.Select(attrs={'class': 'form-select'}), 
            'observaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Observaciones adicionales...', 'class': 'form-control'}),
        }
        labels = {
            'periodo_academico': 'Trimestre',
            'tipo_evaluacion': 'Tipo de Evaluación',
            'asignatura': 'Asignatura / Materia',
            'nombre_actividad': 'Nombre de la Actividad',
        }
    
    def clean_nota(self):
        nota = self.cleaned_data.get('nota')
        if nota is not None:
            if nota < 0 or nota > 10:
                raise ValidationError("La nota debe estar entre 0 y 10")
            if nota < 7:
                observaciones = self.cleaned_data.get('observaciones', '')
                if not observaciones:
                    self.cleaned_data['observaciones'] = 'Nota inferior al aprobatorio.'
        return nota 

class ReporteCalificacionesForm(forms.ModelForm):
    class Meta:
        model = ReporteCalificaciones
        fields = ['titulo', 'tipo_reporte', 'parametros']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ej: Reporte de Calificaciones 2025-I', 'class': 'form-control'}),
            'tipo_reporte': forms.Select(attrs={'class': 'form-control'}),
            'parametros': forms.HiddenInput(),
        }

class FiltroCalificacionesForm(forms.Form):
    ESTADO_CHOICES = [
        ('', 'Todos'),
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('graduado', 'Graduado'),
    ]
    
    año_lectivo = forms.CharField(
        required=False, 
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '2025-2026', 'class': 'form-control'})
    )
    
    periodo_academico = forms.CharField(
        required=False, 
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'T1, T2...', 'class': 'form-control'})
    )
    
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(), 
        required=False,
        empty_label="Todos los cursos",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    estudiante = forms.ModelChoiceField(
        queryset=Estudiante.objects.all(), 
        required=False,
        empty_label="Todos los estudiantes",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    estado_matricula = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        initial='activo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    nota_minima = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00', 'class': 'form-control'})
    )
    
    nota_maxima = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': '10.00', 'class': 'form-control'})
    )
    
    tipo_evaluacion = forms.ChoiceField(
        choices=[('', 'Todos')] + Calificacion._meta.get_field('tipo_evaluacion').choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class BusquedaEstudianteForm(forms.Form):
    termino_busqueda = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por nombre, cédula o código...',
            'class': 'form-control'
        })
    )
    
    año_lectivo = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Filtrar por año lectivo...', 'class': 'form-control'})
    )

class RegistroMultipleCalificacionesForm(forms.Form):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        required=True,
        label="Curso",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo_evaluacion = forms.ChoiceField(
        choices=Calificacion._meta.get_field('tipo_evaluacion').choices,
        required=True,
        label="Tipo de Evaluación",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    periodo_academico = forms.ChoiceField(
        choices=Calificacion.TRIMESTRES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Trimestre"
    )

# =========================================================
# FORMULARIO NUEVO: CONFIGURACIÓN DE PROMEDIOS (70/30)
# =========================================================
class ConfiguracionPromedioForm(forms.Form):
    incluir_examen = forms.BooleanField(
        required=False,
        initial=True,
        label="¿Incluir Examen Quimestral?",
        help_text="Marcar para que el examen cuente en el promedio (si es solo examen, vale el 30%).",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    incluir_proyecto = forms.BooleanField(
        required=False,
        initial=True,
        label="¿Incluir Proyecto Final?",
        help_text="Marcar para que el proyecto cuente en el promedio (si es solo proyecto, vale el 30%).",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        examen = cleaned_data.get('incluir_examen')
        proyecto = cleaned_data.get('incluir_proyecto')

        # Validación: Al menos uno debe estar marcado para tener el 30% restante
        if not examen and not proyecto:
            raise ValidationError("Debes seleccionar al menos una opción (Examen o Proyecto) para completar el 30% restante de la nota.")
            
        return cleaned_data