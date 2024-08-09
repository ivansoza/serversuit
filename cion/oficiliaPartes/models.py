from django.db import models
from catalogos.models import areas, Municipio
from datetime import timedelta
from django.utils import timezone
import os
from datetime import datetime

# Create your models here.
def get_upload_path(instance, filename):
    # Verifica el tipo de instancia
    if isinstance(instance, recepcionDocumentos):
        # Obtener el objeto Area desde recepcionDocumentos
        area = instance.areas
        municipio_nombre = area.municipios_visibles.nombre  # Ajusta según el nombre del campo en tu modelo
        area_nombre = area.Area  # Ajusta según el nombre del campo en tu modelo
    elif isinstance(instance, respuesta):
        # Obtener el objeto recepcionDocumentos desde respuesta
        recepcion_doc = instance.odp
        area = recepcion_doc.areas
        municipio_nombre = area.municipios_visibles.nombre  # Ajusta según el nombre del campo en tu modelo
        area_nombre = area.Area  # Ajusta según el nombre del campo en tu modelo
    else:
        # Proporcionar un valor predeterminado si la instancia no es de un tipo conocido
        municipio_nombre = 'default'
        area_nombre = 'default'

    # Construir la ruta de subida
    return os.path.join(municipio_nombre, 'Archivos Oficiales de partes', area_nombre, filename)
class tipoDocumento(models.Model):
        nombre = models.CharField(max_length=100, unique=True, verbose_name='Tipo de documento')
        def __str__(self):
                return self.nombre
        

# Definición de las opciones para el campo de prioridad
PRIORIDAD_CHOICES = [
    ('ALTA', 'ALTA'),
    ('MEDIA', 'MEDIA'),
    ('BAJA', 'BAJA'),
]    
            
class recepcionDocumentos(models.Model):
    folio_odp = models.CharField(max_length=20, unique=True, blank=True, null=True)
    areas = models.ForeignKey(areas, on_delete=models.CASCADE, verbose_name='Area')
    recibio = models.CharField(max_length=80, verbose_name="Recibió")
    tipo_doc = models.ForeignKey(tipoDocumento, on_delete=models.CASCADE, verbose_name='Tipo de documento')
    prioridad = models.CharField(max_length=50, choices=PRIORIDAD_CHOICES, verbose_name="Prioridad")
    dependencia = models.CharField(max_length=50, verbose_name="Dependencia")
    procedencia = models.CharField(max_length=200, verbose_name="Procedencia")
    folio_expediente = models.CharField(null=True, blank=True, max_length=20, verbose_name='No. folio o expediente')
    archivo = models.FileField(upload_to=get_upload_path, verbose_name='Archivo adjunto', null=True, blank=True,)
    contestacion = models.BooleanField(verbose_name='¿Requiere contestación?')
    horas_asignadas = models.IntegerField(null=True, blank=True, verbose_name='Horas asignadas')
    observaciones = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Campo para fecha de creación
    atendido = models.BooleanField(verbose_name='¿Ya ha sido atendido?', default=False)
    def get_tiempo_restante(self):
        if self.horas_asignadas:
            tiempo_asignado = timedelta(hours=self.horas_asignadas)
            tiempo_transcurrido = timezone.now() - self.fecha_creacion
            tiempo_restante = tiempo_asignado - tiempo_transcurrido
            if tiempo_restante.total_seconds() > 0:
                return int(tiempo_restante.total_seconds())  # Convertir a segundos
        return 0
    
    def save(self, *args, **kwargs):
        municipio_num = kwargs.pop('municipio', None)
        if not self.pk and municipio_num:
            self.folio_odp = self.generate_folio(municipio_num)
        elif not self.pk and not municipio_num:
            raise ValueError("El municipio debe ser proporcionado para generar el folio.")
        super().save(*args, **kwargs)

    def generate_folio(self, municipio_num):
        # Obtener el año actual
        anio_actual = datetime.now().year
        
        # Obtener el número consecutivo
        ultimo_folio = recepcionDocumentos.objects.filter(folio_odp__startswith=f"{municipio_num}/{anio_actual}/").order_by('-id').first()
        ultimo_numero = int(ultimo_folio.folio_odp.split('/')[-1]) if ultimo_folio else 0
        consecutivo = str(ultimo_numero + 1).zfill(2)

        return f"{municipio_num}/{anio_actual}/{consecutivo}"

    def __str__(self):
        return f'{self.tipo_doc} - {self.procedencia}'
    
class respuesta(models.Model):
    odp = models.ForeignKey(recepcionDocumentos, on_delete=models.CASCADE, related_name='atendidos')
    usuario = models.CharField(max_length=250, verbose_name='¿Quien sube respuesta')
    fechaHora = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to=get_upload_path, verbose_name='Respuesta', null=True, blank=True,)
    observaciones = models.TextField(verbose_name='Observaciones', null=True, blank=True)


    def __str__(self):
        return f"{self.usuario} atendió {self.odp} del area {self.odp.areas}"
