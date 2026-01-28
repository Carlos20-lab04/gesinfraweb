from django import forms
from .models import EncuestaAccesibilidad

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = EncuestaAccesibilidad
        fields = '__all__'
        # Widgets para que se vea bonito con Bootstrap
        widgets = {
            'nombre_encuestado': forms.TextInput(attrs={'class': 'form-control'}),
            'interfaz_facilita': forms.Select(attrs={'class': 'form-select'}),
            'afectacion_capacitacion': forms.Select(attrs={'class': 'form-select'}),
            'compatibilidad_equipos': forms.Select(attrs={'class': 'form-select'}),
            'identifica_soporte': forms.Select(attrs={'class': 'form-select'}),
            'desplazamiento_autonomo': forms.Select(attrs={'class': 'form-select'}),
            'elementos_apoyo': forms.Select(attrs={'class': 'form-select'}),
            'recursos_accesibles': forms.Select(attrs={'class': 'form-select'}),
            'docentes_inclusivos': forms.Select(attrs={'class': 'form-select'}),
            'contenidos_adaptados': forms.Select(attrs={'class': 'form-select'}),
            'materiales_accesibles': forms.Select(attrs={'class': 'form-select'}),
            'barrera_frecuente': forms.Select(attrs={'class': 'form-select'}),
            'politicas_claras': forms.Select(attrs={'class': 'form-select'}),
            'capacitacion_docente': forms.Select(attrs={'class': 'form-select'}),
            'conocimiento_bap': forms.Select(attrs={'class': 'form-select'}),
        }