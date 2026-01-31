from django import forms
from .models import EncuestaAccesibilidad

class EncuestaAccesibilidadForm(forms.ModelForm):
    class Meta:
        model = EncuestaAccesibilidad
        fields = '__all__'
        # Los widgets definen que sea un menú desplegable (Select)
        widgets = {
            'nombre_encuestado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'q1_interfaz': forms.Select(attrs={'class': 'form-select'}),
            'q2_capacitacion': forms.Select(attrs={'class': 'form-select'}),
            'q3_compatibilidad': forms.Select(attrs={'class': 'form-select'}),
            'q4_soporte': forms.Select(attrs={'class': 'form-select'}),
            'q5_instalaciones': forms.Select(attrs={'class': 'form-select'}),
            'q6_apoyo': forms.Select(attrs={'class': 'form-select'}),
            'q7_recursos_tec': forms.Select(attrs={'class': 'form-select'}),
            'q8_metodologias': forms.Select(attrs={'class': 'form-select'}),
            'q9_materiales': forms.Select(attrs={'class': 'form-select'}),
            'q10_adaptaciones': forms.Select(attrs={'class': 'form-select'}),
            'q11_barreras': forms.Select(attrs={'class': 'form-select'}),
            'q12_politicas': forms.Select(attrs={'class': 'form-select'}),
            'q13_capacitacion_inst': forms.Select(attrs={'class': 'form-select'}),
            'q14_conocimiento_bap': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorremos todos los campos para quitar la opción "---------"
        for field_name, field in self.fields.items():
            if field_name != 'nombre_encuestado':
                # Si el campo tiene opciones y la primera es vacía (las rayitas), la borramos
                if field.choices and field.choices[0][0] == '':
                    field.choices = field.choices[1:]