from django.db import models
from catalogos.models import Autoridad,areas
from datetime import timedelta, datetime
from django.db import models

class tipoDocumento(models.Model):
        nombre = models.CharField(max_length=100, unique=True, verbose_name='Tipo de documento')
        def __str__(self):
                return self.nombre
        

# Definición de las opciones para el campo de prioridad
PRIORIDAD_CHOICES = [
    ('Alta', 'ALTA'),
    ('media', 'MEDIA'),
    ('baja', 'BAJA'),
]    
            
class ODP(models.Model):
    areas = models.ForeignKey(areas, on_delete=models.CASCADE, related_name='Areas')
    tipo_doc = models.ForeignKey(tipoDocumento, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo de documento')
    procedencia = models.CharField(max_length=200, verbose_name="Procedencia")
    prioridad = models.CharField(max_length=50, choices=PRIORIDAD_CHOICES, verbose_name="Prioridad")
    dependencia = models.CharField(max_length=50, verbose_name="Dependencia")
    recibio = models.CharField(max_length=80, verbose_name="Recibío")
    observaciones = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    folio = models.CharField(null=True, blank=True, max_length=20, verbose_name='No. folio')
    archivo = models.FileField(upload_to='uploads/', verbose_name='Archivo adjunto', null=True, blank=True,)
    status = models.BooleanField(default=False, verbose_name='Estado')
    contestacion = models.BooleanField(default=False, verbose_name='contestación')
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Campo para fecha de creación
    horas_asignadas = models.IntegerField(null=True, blank=True, verbose_name='Horas asignadas')

    def get_tiempo_restante(self):
        if self.horas_asignadas:
            tiempo_asignado = timedelta(hours=self.horas_asignadas)
            tiempo_transcurrido = timezone.now() - self.fecha_creacion
            tiempo_restante = tiempo_asignado - tiempo_transcurrido
            if tiempo_restante.total_seconds() > 0:
                return int(tiempo_restante.total_seconds())  # Convertir a segundos
        return 0
    def __str__(self):
        return f'{self.tipo_doc} - {self.procedencia}'

from django.utils import timezone

class Atendido(models.Model):
    odp = models.ForeignKey(ODP, on_delete=models.CASCADE, related_name='atendidos')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    archivo = models.FileField(upload_to='uploads/', verbose_name='Respuesta', null=True, blank=True,)


    def __str__(self):
        return f"{self.nombre} {self.apellido} atendió {self.odp} del area {self.odp.areas}"


class RevisionPropuesta(models.Model):
    propuesta = models.ForeignKey(Atendido, on_delete=models.CASCADE, related_name='propuesta')
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    acepta = models.BooleanField(default=False, verbose_name='Aceptar respuesta')
    noacepta = models.BooleanField(default=False, verbose_name='No aceptar respuesta')
    observaciones = models.TextField(verbose_name='Observaciones', null=True, blank=True)

 
    def __str__(self):
        return str(self.propuesta)  # Esto es correcto si 'propuesta' es un campo del modelo


