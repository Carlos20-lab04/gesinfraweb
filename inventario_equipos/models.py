from django.db import models

# ==========================================
# 1. MODELO DE EQUIPOS
# ==========================================
class Equipo(models.Model):
    TIPO_EQUIPO_CHOICES = [
        ('computadora', 'Computadora'),
        ('laptop', 'Laptop'),
        ('servidor', 'Servidor'),
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('impresora', 'Impresora'),
        ('proyector', 'Proyector'),
        ('tablet', 'Tablet'),
        ('otros', 'Otros'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('baja', 'Dado de Baja'),
    ]
    
    # Se añade blank=True y null=True para que NO sean obligatorios al guardar
    # Se eliminó 'unique=True' para evitar errores al dejar varios en blanco
    codigo_inventario = models.CharField(max_length=50, blank=True, null=True)
    tipo_equipo = models.CharField(max_length=20, choices=TIPO_EQUIPO_CHOICES, default='computadora')
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, blank=True, null=True)
    responsable = models.CharField(max_length=100, blank=True, null=True, verbose_name="Responsable del Equipo")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_adquisicion = models.DateField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    especificaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo_equipo} {self.marca} {self.modelo}"

# ==========================================
# 2. MODELO DE MANTENIMIENTOS
# ==========================================
class Mantenimiento(models.Model):
    TIPO_MANTENIMIENTO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
        ('diagnostico', 'Diagnóstico'),
    ]
    
    ESTADO_MANTENIMIENTO_CHOICES = [
        ('programado', 'Programado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_mantenimiento = models.DateField()
    tipo_mantenimiento = models.CharField(max_length=20, choices=TIPO_MANTENIMIENTO_CHOICES)
    descripcion = models.TextField()
    tecnico = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_MANTENIMIENTO_CHOICES)
    fecha_proximo_mantenimiento = models.DateField(null=True, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank= True )
    
    def __str__(self):
        return f"Mantenimiento {self.tipo_mantenimiento} - {self.equipo}"

# ==========================================
# 3. MODELO DE REDES
# ==========================================
class Red(models.Model):
    TIPO_RED_CHOICES = [
        ('lan', 'LAN'),
        ('wlan', 'WLAN'),
        ('wan', 'WAN'),
    ]
    
    ESTADO_RED_CHOICES = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    nombre_red = models.CharField(max_length=100)
    tipo_red = models.CharField(max_length=10, choices=TIPO_RED_CHOICES)
    
    # Se añade null=True y blank=True también aquí por si quieres guardar redes rápido
    direccion_ip = models.GenericIPAddressField(blank=True, null=True)
    mascara_subred = models.GenericIPAddressField(blank=True, null=True)
    gateway = models.GenericIPAddressField(blank=True, null=True)
    dns = models.GenericIPAddressField(blank=True, null=True)
    
    estado = models.CharField(max_length=20, choices=ESTADO_RED_CHOICES, default='activa')
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    equipos_conectados = models.ManyToManyField(Equipo, blank=True)
    
    def __str__(self):
        return self.nombre_red