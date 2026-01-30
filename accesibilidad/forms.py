from django import forms
from .models import EncuestaAccesibilidad

class EncuestaAccesibilidadForm(forms.ModelForm):
    class Meta:
        model = EncuestaAccesibilidad
        fields = '__all__'
        
        # Esto convierte las listas desplegables en opciones de "bolita" (Radio Buttons)
        widgets = {
            'q1_interfaz': forms.RadioSelect,
            'q2_capacitacion': forms.RadioSelect,
            'q3_compatibilidad': forms.RadioSelect,
            'q4_soporte': forms.RadioSelect,
            'q5_instalaciones': forms.RadioSelect,
            'q6_apoyo': forms.RadioSelect,
            'q7_recursos_tec': forms.RadioSelect,
            'q8_metodologias': forms.RadioSelect,
            'q9_materiales': forms.RadioSelect,
            'q10_adaptaciones': forms.RadioSelect,
            'q11_barreras': forms.RadioSelect,
            'q12_politicas': forms.RadioSelect,
            'q13_capacitacion_inst': forms.RadioSelect,
            'q14_conocimiento_bap': forms.RadioSelect,
            
            # Ocultamos el campo de fecha porque es automático
            'fecha': forms.HiddenInput(),
            
            # Estilo para el nombre (opcional)
            'nombre_encuestado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre (Opcional)'}),
        }