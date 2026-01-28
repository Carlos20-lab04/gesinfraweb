from django.contrib import admin
from .models import EncuestaAccesibilidad

@admin.register(EncuestaAccesibilidad)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ('nombre_encuestado', 'fecha')