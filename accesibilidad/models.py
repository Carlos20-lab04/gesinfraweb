from django.db import models

class EncuestaAccesibilidad(models.Model):
    # Opciones
    OPCIONES_FRECUENCIA = [('siempre', 'Siempre'), ('casi_siempre', 'Casi siempre'), ('a_veces', 'A veces'), ('rara_vez', 'Rara vez'), ('nunca', 'Nunca')]
    OPCIONES_AFIRMACION = [('si', 'Sí'), ('no', 'No'), ('parcialmente', 'Parcialmente'), ('tal_vez', 'Tal vez'), ('desconozco', 'Desconozco')]
    OPCIONES_CAPACITACION = [('obstaculo', 'Ha sido un obstáculo total'), ('dificultad', 'Me ha dificultado algunas cosas'), ('perdido', 'A veces me siento perdido'), ('sin_problemas', 'He podido manejarlo sin problemas')]
    OPCIONES_COMPATIBILIDAD = [('si', 'Sí'), ('lento', 'A veces falla o es lento'), ('inestable', 'Funciona de forma inestable'), ('no_soporta', 'Mi equipo no soporta la plataforma')]
    OPCIONES_BARRERAS = [('metodologias', 'Metodologías homogéneas'), ('recursos', 'Falta de recursos didácticos accesibles'), ('evaluaciones', 'Evaluaciones no adaptadas')]

    # Campos
    fecha = models.DateTimeField(auto_now_add=True)
    nombre_encuestado = models.CharField(max_length=100, verbose_name="Nombre del Participante")

    # Sección 1
    interfaz_facilita = models.CharField(max_length=20, choices=OPCIONES_AFIRMACION, verbose_name="1. ¿La interfaz facilita localizar herramientas?")
    afectacion_capacitacion = models.CharField(max_length=20, choices=OPCIONES_CAPACITACION, verbose_name="2. ¿Cómo afecta la falta de capacitación?")
    compatibilidad_equipos = models.CharField(max_length=20, choices=OPCIONES_COMPATIBILIDAD, verbose_name="3. Nivel de compatibilidad de dispositivos")
    identifica_soporte = models.CharField(max_length=20, choices=OPCIONES_AFIRMACION, verbose_name="4. ¿Identifica canales de soporte técnico?")

    # Sección 2
    desplazamiento_autonomo = models.CharField(max_length=20, choices=OPCIONES_FRECUENCIA, verbose_name="5. ¿Instalaciones permiten desplazamiento autónomo?")
    elementos_apoyo = models.CharField(max_length=20, choices=OPCIONES_AFIRMACION, verbose_name="6. ¿Cuenta con rampas, ascensores, señalética?")
    recursos_accesibles = models.CharField(max_length=20, choices=OPCIONES_FRECUENCIA, verbose_name="7. ¿Laboratorios/Plataformas son accesibles?")

    # Sección 3
    docentes_inclusivos = models.CharField(max_length=20, choices=OPCIONES_FRECUENCIA, verbose_name="8. ¿Docentes aplican metodologías inclusivas?")
    contenidos_adaptados = models.CharField(max_length=20, choices=OPCIONES_AFIRMACION, verbose_name="9. ¿Contenidos toman en cuenta necesidades educativas?")
    materiales_accesibles = models.CharField(max_length=20, choices=OPCIONES_FRECUENCIA, verbose_name="10. ¿Se utilizan materiales adaptados?")
    barrera_frecuente = models.CharField(max_length=20, choices=OPCIONES_BARRERAS, verbose_name="11. ¿Qué barrera identifica con mayor frecuencia?")

    # Sección 4
    politicas_claras = models.CharField(max_length=20, choices=OPCIONES_AFIRMACION, verbose_name="12. ¿Políticas claras sobre inclusión?")
    capacitacion_docente = models.CharField(max_length=20, choices=[('si', 'Sí'), ('no', 'No'), ('poca', 'Muy poca')], verbose_name="13. ¿Proceso de capacitación a docentes?")
    conocimiento_bap = models.CharField(max_length=20, choices=OPCIONES_AFIRMACION, verbose_name="14. ¿Conocimiento sobre Barreras de Aprendizaje (BAP)?")

    def __str__(self):
        return f"{self.nombre_encuestado} - {self.fecha.strftime('%d/%m/%Y')}"