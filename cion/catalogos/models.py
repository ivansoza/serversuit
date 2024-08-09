from django.db import models
import os
# Create your models here.
from django.db.models import Q


class Estado(models.Model):
    numero_estado = models.IntegerField(default=1)  # Ajusta el valor por defecto según tu lógica de negocio
    nombre = models.CharField(max_length=100, verbose_name="Nombre")

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    numero_municipio =  models.IntegerField(default=1) 
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado")

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return self.nombre
    
class Colonia(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Colonia")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='colonias', verbose_name="Municipio")

    class Meta:
        verbose_name = "Colonia"
        verbose_name_plural = "Colonias"

    def __str__(self):
        return self.nombre
    
class Calle(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Calle")
    colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE, related_name='calles', verbose_name="Colonia")

    class Meta:
        verbose_name = "Calle"
        verbose_name_plural = "Calles"

    def __str__(self):
        return self.nombre
def get_upload_path(instance, filename):
    # Construir la ruta de subida basada en el nombre del municipio
    return os.path.join(instance.municipio.nombre, 'logotipos_municipios', filename)

class PersonalizacionTema(models.Model):
    municipio = models.OneToOneField(Municipio, on_delete=models.CASCADE, related_name="personalizacion", unique=True)
    TIPO_DISENO_CHOICES = [
        ('LTR', 'Left-to-Right'),
        ('RTL', 'Right-to-Left'),
        ('BOX', 'Boxed')
    ]
    tipo_diseno = models.CharField(max_length=23, choices=TIPO_DISENO_CHOICES, verbose_name="Tipo de Diseño", null=True, blank=True)
    TIPO_SIDEBAR_CHOICES = [
        ('NORMAL-SIDEBAR', 'Top Sidebar'),
        ('COMPACT-SIDEBAR', 'Left Sidebar')
    ]
    tipo_sidebar = models.CharField(max_length=15, choices=TIPO_SIDEBAR_CHOICES, verbose_name="Tipo de Sidebar", null=True, blank=True)
    TIPO_ICONO_SIDEBAR_CHOICES = [
        ('STROKE-SVG', 'Stroke Icons'),
        ('FILL-SVG', 'Fill Icons')
    ]
    tipo_icono_sidebar = models.CharField(max_length=12, choices=TIPO_ICONO_SIDEBAR_CHOICES, verbose_name="Tipo de Icono para el Sidebar", null=True, blank=True)
    color_1 = models.CharField(max_length=7, verbose_name="Color Claro", help_text="Código hexadecimal del color claro", null=True, blank=True)
    color_1a = models.CharField(max_length=7, verbose_name="Color primario 1", help_text="Código hexadecimal del color 1", null=True, blank=True)
    color_2 = models.CharField(max_length=7, verbose_name="Color Oscuro", help_text="Código hexadecimal del color oscuro", null=True, blank=True)
    color_2a = models.CharField(max_length=7, verbose_name="Color secundario1", help_text="Código hexadecimal del color 1", null=True, blank=True)
    logotipo = models.ImageField(
        upload_to=get_upload_path,
        verbose_name="Logotipo del Municipio",
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = "Personalización de Tema"
        verbose_name_plural = "Personalizaciones de Temas"

    def __str__(self):
        return f"Personalización para {self.municipio.nombre}"
    

class tipoServicioAgua(models.Model):
    tipoServicio = models.CharField(max_length=150, verbose_name='Tipo de servicio')    
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    def __str__(self):
        return self.tipoServicio


class areas(models.Model):
    Area = models.CharField(max_length=100, verbose_name='Area')
    municipios_visibles = models.ForeignKey(Municipio, on_delete=models.CASCADE, blank=True, null=True, related_name='municipios_visibles', verbose_name='Municipios Visibles')
    
    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return self.Area

    def es_general(self):
        return self.municipios_visibles is None

    def visible_para_municipio(self, municipio):
        return self.municipios_visibles == municipio if municipio else self.es_general()

    @classmethod
    def obtener_areas_visibles(cls, usuario):
        municipio_usuario = usuario.id  # Aquí estás intentando acceder correctamente al municipio del usuario
        if municipio_usuario:
            return cls.objects.filter(models.Q(municipios_visibles=None) | models.Q(municipios_visibles=municipio_usuario))
        else:
            return cls.objects.filter(municipios_visibles=None)
        
        
    @classmethod
    def obtener_areas_visiblesMunicipio(cls, usuario):
        municipio_usuario = usuario.Municipio  # Aquí estás intentando acceder correctamente al municipio del usuario
        if municipio_usuario:
            return cls.objects.filter(models.Q(municipios_visibles=None) | models.Q(municipios_visibles=municipio_usuario))
        else:
            return cls.objects.filter(municipios_visibles=None)


class areasMunicipio(models.Model):
    area = models.ManyToManyField(areas,  blank=True, verbose_name='Areas')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    
    def __str__(self):
        return f'{self.area}'

class  Autoridad (models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    nombreAutoridad = models.CharField(max_length=100, verbose_name='Autoridad')
    
    class Meta:
        verbose_name ='Autoridad'
        verbose_name_plural = 'Autoridad'
        
    def __str__(self):
        return self.nombreAutoridad
    
class Servicios(models.Model):
    codigoServicio = models.CharField(max_length=10, verbose_name='Código de servicio')
    descripcion = models.CharField(max_length=300, verbose_name='Descripción del servicio')
    claveProducto = models.CharField(max_length=300, verbose_name='Clave del producto', blank=True, null=True)
    fecha_inicio = models.DateField(verbose_name='Fecha inicio', blank=True, null=True)
    fecha_fin = models.DateField(verbose_name='Fecha Fin', blank=True, null=True)
    estatus = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.codigoServicio} - {self.descripcion}"

    class Meta:
            ordering = ['codigoServicio'] 

    
class Descuentos(models.Model):
    tipo = models.CharField(max_length=9,default='DESCUENTO')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    monto_descuento = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Monto de descuento')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    ESTATUS_CHOICES = [
        ('ACTIVO', 'ACTIVO'),
        ('INACTIVO', 'INACTIVO')
    ]
    estatus_descuento = models.CharField(max_length=8, choices=ESTATUS_CHOICES, default='ACTIVO')
    def __str__(self) -> str:
        return self.nombre
    
class Recargos(models.Model):
    tipo = models.CharField(max_length=9,default='RECARGO')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    monto_recargo = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Monto de recargo')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    ESTATUS_RE_CHOICES = [
        ('ACTIVO', 'ACTIVO'),
        ('INACTIVO', 'INACTIVO')
    ]
    estatus_recargos = models.CharField(max_length=8, choices=ESTATUS_RE_CHOICES, default='ACTIVO')
    def __str__(self) -> str:
        return self.nombre
    
class ServicioMunicipio(models.Model):
    clave = models.ForeignKey(Servicios, on_delete=models.CASCADE, verbose_name='Servicio')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    concepto = models.CharField(max_length=200, verbose_name='Concepto')
    monto = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Monto')
    area = models.ForeignKey(areas, on_delete=models.CASCADE, verbose_name='Área')  # Cambiado a areas

    def __str__(self):
        return f"{self.clave} - {self.municipio}"