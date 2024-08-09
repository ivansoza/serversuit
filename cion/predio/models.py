from django.db import models

from catalogos.models import Calle, Colonia, Municipio
from contribuyente.models import Contribuyente

# Create your models here.

class predio(models.Model):
    contribuyente = models.ForeignKey(Contribuyente, on_delete=models.CASCADE, related_name='prediocontribuyente')

    USO_PREDIO_CHOICES = [
        ('URB', 'Urbano'),
        ('RUS', 'Rústico'),
        ('COM', 'Comercial'),
    ]
    colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE, null=True, verbose_name="Colonia")

    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    calle = models.ForeignKey(Calle,on_delete=models.CASCADE, null=True, verbose_name="Calle")

    nombre = models.CharField(max_length=18, blank=True, null=True)
    razonSocial = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, verbose_name='EMAIL', blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    
    curp = models.CharField(max_length=18, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    homoclave = models.CharField(max_length=3, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    ApellidoP = models.CharField(max_length=100)
    ApellidoM = models.CharField(max_length=100)
    nombre_mc = models.CharField(max_length=100, blank=True, null=True)
    ApellidoP_mc = models.CharField(max_length=100, blank=True, null=True)
    ApellidoM_mc = models.CharField(max_length=100, blank=True, null=True)
    clave_catastral = models.CharField(max_length=20, unique=True)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    numero_exterior = models.CharField(max_length=10, blank=True, null=True)
    numero_interior = models.CharField(max_length=10, blank=True, null=True)
    superficie_total = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    superficie_construida = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    uso_predio = models.CharField(max_length=3, choices=USO_PREDIO_CHOICES)
    valor_catastral = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, default='Activo')  # Activo, Inactivo, etc.
    fecha_registro = models.DateTimeField(auto_now_add=True)
    registro = models.CharField(max_length=200, verbose_name='Quien registro')
    

    class Meta:
        verbose_name = "Predio"
        verbose_name_plural = "Predios"
        unique_together = (('municipio', 'clave_catastral'),)

    def __str__(self):
        return f"{self.clave_catastral} - {self.contribuyente.nombre}"

    def obtener_nombre(self):
        """
        Devuelve el nombre completo o razón social del contribuyente asociado a este predio,
        dependiendo de si el contribuyente es persona física o moral.
        """
        contrib = self.contribuyente
        if contrib.tipoPersona == 'PM':  # Persona Moral
            return self.razonSocial.upper() if self.razonSocial else "RAZÓN SOCIAL NO DISPONIBLE"
        else:  # Persona Física
            # Construye el nombre completo evitando incluir partes del nombre que son None o vacías.
            partes_nombre = [self.nombre, self.ApellidoP, self.ApellidoM]
            # Filtra las partes que no están vacías y las une con espacio.
            nombre_completo = " ".join([parte for parte in partes_nombre if parte])
            return nombre_completo
        
