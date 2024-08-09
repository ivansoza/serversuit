from django.db import models
import os
from catalogos.models import Municipio
def get_upload_path(instance, filename):
    # Construir la ruta de subida basada en el nombre del municipio
    return os.path.join(instance.municipio.nombre, 'logotipos_municipios', filename)
# Create your models here.
class PaginaInicio(models.Model):
    titulo = models.CharField(max_length=100, verbose_name='Identificación', null=True, blank=True)
    imagen_inicio = models.ImageField(upload_to=get_upload_path,verbose_name='Imagen del home', null=True, blank=True)
    mapa_html = models.TextField(blank=True, null=True)
    mision = models.TextField(
        blank=True, 
        null=True
    )
    vision = models.TextField(
        blank=True, 
        null=True
    )
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    telefono = models.CharField(
        max_length=13, 
        verbose_name='Teléfono', 
        blank=True, 
        null=True
    )
    email = models.EmailField(
        verbose_name='Email', 
        blank=True, 
        null=True
    )
    direccion = models.CharField(
        max_length=90, 
        verbose_name='Dirección', 
        blank=True, 
        null=True
    )
    imagen_organigrama = models.ImageField(upload_to=get_upload_path,verbose_name='Imagen organigrama', null=True, blank=True)

    def __str__(self):
        return "Página de Inicio"

    class Meta:
        verbose_name = "Página de Inicio"
        verbose_name_plural = "Páginas de Inicio"

