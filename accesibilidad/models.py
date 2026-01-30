from django.db import models

class EncuestaAccesibilidad(models.Model):
    # --- DEFINICIÓN DE OPCIONES EXACTAS SEGÚN TU SOLICITUD ---

    # Para preguntas de Si/No/Tal vez/Parcialmente (Preguntas 1 y 14)
    OPCIONES_NIVEL_AFIRMACION = [
        ('Si', 'Si'),
        ('Parcialmente', 'Parcialmente'),
        ('Tal vez', 'Tal vez'),
        ('No', 'No')
    ]

    # Para pregunta 2 (Capacitación tecnológica)
    OPCIONES_CAPACITACION_TEC = [
        ('Obstaculo', 'Ha sido un obstáculo total'),
        ('Dificultad', 'Me ha dificultado algunas cosas'),
        ('Perdido', 'A veces me siento perdido'),
        ('SinProblemas', 'He podido manejarlo sin problemas')
    ]

    # Para pregunta 3 (Compatibilidad)
    OPCIONES_COMPATIBILIDAD = [
        ('Si', 'Si'),
        ('Lento', 'A veces falla o es lento'),
        ('Inestable', 'Funciona de forma inestable'),
        ('NoSoporta', 'Mi equipo no soporta la plataforma')
    ]

    # Para pregunta 4 (Soporte)
    OPCIONES_SOPORTE = [
        ('Si', 'Si'),
        ('No', 'No'),
        ('Tal vez', 'Tal vez')
    ]

    # Para frecuencias de infraestructura (Pregunta 5)
    OPCIONES_FRECUENCIA_INFRA = [
        ('Siempre', 'Siempre'),
        ('Casi siempre', 'Casi siempre'),
        ('A veces', 'A veces'),
        ('Nunca', 'Nunca')
    ]

    # Para preguntas de Sí/No/Parcialmente (Preguntas 6 y 9)
    OPCIONES_SI_NO_PARCIAL = [
        ('Si', 'Sí'),
        ('No', 'No'),
        ('Parcialmente', 'Parcialmente')
    ]

    # Para preguntas de Siempre/A veces/Nunca (Preguntas 7, 10)
    OPCIONES_SIEMPRE_AVECES_NUNCA = [
        ('Siempre', 'Siempre'),
        ('A veces', 'A veces'),
        ('Nunca', 'Nunca')
    ]

    # Para pregunta 8 (Metodologías - incluye "Rara vez")
    OPCIONES_DOCENTES = [
        ('Siempre', 'Siempre'),
        ('A veces', 'A veces'),
        ('Rara vez', 'Rara vez'),
        ('Nunca', 'Nunca')
    ]

    # Para pregunta 11 (Barreras Pedagógicas)
    OPCIONES_BARRERAS = [
        ('Metodologias', 'Metodologías homogéneas'),
        ('Recursos', 'Falta de recursos didácticos accesibles'),
        ('Evaluaciones', 'Evaluaciones no adaptadas')
    ]

    # Para pregunta 12 (Políticas - incluye "Desconozco")
    OPCIONES_POLITICAS = [
        ('Si', 'Sí'),
        ('No', 'No'),
        ('Desconozco', 'Desconozco')
    ]

    # Para pregunta 13 (Capacitación Inst - incluye "Muy poca")
    OPCIONES_CAPACITACION_INST = [
        ('Si', 'Sí'),
        ('No', 'No'),
        ('Muy poca', 'Muy poca')
    ]

    # --- CAMPOS DEL MODELO ---
    
    fecha = models.DateTimeField(auto_now_add=True)
    # Opcional: Nombre del encuestado (puedes quitarlo si la encuesta es anónima)
    nombre_encuestado = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre (Opcional)")

    # === SECCIÓN 1: BARRERAS TECNOLÓGICAS ===
    q1_interfaz = models.CharField(
        max_length=20, choices=OPCIONES_NIVEL_AFIRMACION, 
        verbose_name="1. ¿La interfaz facilita la localización de herramientas?"
    )
    q2_capacitacion = models.CharField(
        max_length=20, choices=OPCIONES_CAPACITACION_TEC, 
        verbose_name="2. Ausencia de capacitación sobre uso de tecnología"
    )
    q3_compatibilidad = models.CharField(
        max_length=20, choices=OPCIONES_COMPATIBILIDAD, 
        verbose_name="3. Nivel de compatibilidad de dispositivos"
    )
    q4_soporte = models.CharField(
        max_length=20, choices=OPCIONES_SOPORTE, 
        verbose_name="4. ¿Identifica canales de soporte técnico?"
    )

    # === SECCIÓN 2: BARRERAS DE INFRAESTRUCTURA ===
    q5_instalaciones = models.CharField(
        max_length=20, choices=OPCIONES_FRECUENCIA_INFRA, 
        verbose_name="5. ¿Instalaciones permiten desplazamiento autónomo?"
    )
    q6_apoyo = models.CharField(
        max_length=20, choices=OPCIONES_SI_NO_PARCIAL, 
        verbose_name="6. Elementos de apoyo (rampas, ascensores, señalética)"
    )
    q7_recursos_tec = models.CharField(
        max_length=20, choices=OPCIONES_SIEMPRE_AVECES_NUNCA, 
        verbose_name="7. ¿Recursos tecnológicos son accesibles?"
    )

    # === SECCIÓN 3: BARRERAS PEDAGÓGICAS ===
    q8_metodologias = models.CharField(
        max_length=20, choices=OPCIONES_DOCENTES, 
        verbose_name="8. ¿Docentes aplican metodologías inclusivas?"
    )
    q9_materiales = models.CharField(
        max_length=20, choices=OPCIONES_SI_NO_PARCIAL, 
        verbose_name="9. ¿Contenidos diseñados para diversas necesidades?"
    )
    q10_adaptaciones = models.CharField(
        max_length=20, choices=OPCIONES_SIEMPRE_AVECES_NUNCA, 
        verbose_name="10. ¿Se utilizan adaptaciones curriculares?"
    )
    q11_barreras = models.CharField(
        max_length=20, choices=OPCIONES_BARRERAS, 
        verbose_name="11. Barreras pedagógicas más frecuentes"
    )

    # === SECCIÓN 4: BARRERAS POLÍTICAS Y DE GESTIÓN ===
    q12_politicas = models.CharField(
        max_length=20, choices=OPCIONES_POLITICAS, 
        verbose_name="12. ¿Políticas claras sobre inclusión?"
    )
    q13_capacitacion_inst = models.CharField(
        max_length=20, choices=OPCIONES_CAPACITACION_INST, 
        verbose_name="13. ¿Capacitación institucional a docentes?"
    )
    q14_conocimiento_bap = models.CharField(
        max_length=20, choices=OPCIONES_NIVEL_AFIRMACION, 
        verbose_name="14. ¿Conocimiento sobre Barreras BAP?"
    )

    def __str__(self):
        return f"Encuesta #{self.id} - {self.fecha.strftime('%d/%m/%Y')}"