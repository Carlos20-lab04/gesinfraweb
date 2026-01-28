from django import forms
from .models import Equipo, Mantenimiento, Red

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'
        widgets = {
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'especificaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        # --- CAMBIO IMPORTANTE ---
        # Usamos 'exclude' para ocultar el costo del formulario.
        # Como ya lo hiciste opcional en la BD, se guardará como vacío (NULL) sin dar error.
        exclude = ['costo']
        
        widgets = {
            # Mantengo tus nombres de campos y agrego clases para diseño
            'fecha_mantenimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_proximo_mantenimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            # Agrego estos dos por seguridad (por si tu modelo usa estos nombres en vez de los de arriba)
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'proxima_revision': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tecnico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del técnico'}),
            'tecnico_responsable': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Esto evita errores si el navegador manda la fecha en un formato distinto
        date_fields = ['fecha_mantenimiento', 'fecha_proximo_mantenimiento', 'fecha_inicio', 'proxima_revision']
        for field in date_fields:
            if field in self.fields:
                self.fields[field].input_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']

class RedForm(forms.ModelForm):
    class Meta:
        model = Red
        fields = '__all__'