from django.db import models
from predio.models import predio
from catalogos.models import tipoServicioAgua, Municipio
from contribuyente.models import Contribuyente
from predio.models import predio
from catalogos.models import Calle, Colonia, Municipio

class TipoContrato(models.Model):
    tipo = models.CharField(max_length=50, verbose_name='Tipo de contrato')
    def __str__(self):
        return self.tipo
class noServicio(models.Model):
    # Datos del contribuyente----------------------------------------------
    contri = models.ForeignKey(Contribuyente, on_delete=models.CASCADE, verbose_name='Contribuyente',related_name='noservicios')

    rfc = models.CharField(max_length=10, verbose_name='RFC')
    homoclave = models.CharField(max_length=3, null=True, blank=True)
    curp = models.CharField(max_length=18, verbose_name='CURP', blank=True, null=True)
    tipoPersona = models.CharField(max_length=2, choices=[('PF', 'PERSONA FÍSICA'), ('PM', 'PERSONA MORAL')], verbose_name='Tipo de Persona')
    nombre = models.CharField(max_length=100, blank=True, null=True)
    ApellidoP = models.CharField(max_length=100, blank=True, null=True)
    ApellidoM = models.CharField(max_length=100, blank=True, null=True)
    razonSocial = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, verbose_name='EMAIL', blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    # Bienes mancomunados
    nombre_mc = models.CharField(max_length=100, blank=True, null=True)
    ApellidoP_mc = models.CharField(max_length=100, blank=True, null=True)
    ApellidoM_mc = models.CharField(max_length=100, blank=True, null=True)
    # Datos de predio------------------------------------------------------
    claveCatastral = models.CharField(max_length=20, verbose_name='Clave Catastral', blank=True, null=True)    
    estado = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=5, blank=True, null=True)
    municipio_predio = models.CharField(max_length=100, verbose_name='Municipio Predio', blank=True, null=True)
    colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE, null=True, verbose_name="Colonia", blank=True)
    calle = models.ForeignKey(Calle,on_delete=models.CASCADE, null=True, verbose_name="Calle", blank=True)
    numero_exterior = models.CharField(max_length=10, blank=True, null=True)
    numero_interior = models.CharField(max_length=10, blank=True, null=True)
    superficie_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    superficie_construida = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    uso_predio= models.CharField(max_length=3, choices=[('URB', 'Urbano'),('RUS', 'Rústico'),('COM', 'Comercial'),], blank=True, null=True)
    valor_catastral = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    # Datos del servicio de agua potable
    noServicio = models.CharField(max_length=20, verbose_name='No. de servicio')
    tipoServicio = models.ForeignKey(tipoServicioAgua, on_delete=models.CASCADE, verbose_name='Tipo de servicio')
    fecha_hora = models.DateTimeField(auto_now=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    registro = models.CharField(max_length=200, verbose_name='Quien registro')
    predio = models.ForeignKey(predio, on_delete=models.CASCADE, verbose_name='Predio', null=True, blank=True)
    def __str__(self):
        return self.noServicio