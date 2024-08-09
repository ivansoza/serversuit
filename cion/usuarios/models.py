from django.db import models
from django.contrib.auth.models import AbstractUser
from catalogos.models import Municipio, areasMunicipio,areas
# Create your models here.
class CustomUser(AbstractUser):
    SEXO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
    ]
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, null=True, blank=True)
    Municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
    areas = models.ManyToManyField(areas, blank=True, verbose_name='Áreas')
    es_responsable = models.BooleanField(default=False, verbose_name='¿Es responsable?')


    def __str__(self):
        return self.username
    apellido_materno = models.CharField(max_length=100, blank=True)
