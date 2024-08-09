from django.db import models

from catalogos.models import Calle, Colonia, Municipio

class Contribuyente(models.Model):
    PERSONA_FISICA = 'PF'
    PERSONA_MORAL = 'PM'
    TIPO_PERSONA_CHOICES = [
        (PERSONA_FISICA, 'PERSONA FÍSICA'),
        (PERSONA_MORAL, 'PERSONA MORAL'),
    ]

    tipoPersona = models.CharField(
        max_length=2,
        choices=TIPO_PERSONA_CHOICES,
        default=PERSONA_FISICA,
    )
    mc = models.BooleanField(default=False)

    # Domicilio
    calle = models.ForeignKey(Calle,on_delete=models.CASCADE, null=True, verbose_name="Calle")
    numeroE = models.CharField(max_length=10, blank=True, null=True)
    numeroI = models.CharField(max_length=10, blank=True, null=True)
    cp = models.CharField(max_length=5, blank=True, null=True)
    colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE, null=True, verbose_name="Colonia")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    
    # Informacion del contribuyente 
    curp = models.CharField(max_length=18, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellidoP = models.CharField(max_length=100, blank=True, null=True)
    apellidoM = models.CharField(max_length=100, blank=True, null=True)
    razonSocial = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    # Bienes mancomunados
    nombre_mc = models.CharField(max_length=100, blank=True, null=True)
    apellidoP_mc = models.CharField(max_length=100, blank=True, null=True)
    apellidoM_mc = models.CharField(max_length=100, blank=True, null=True)


    
    estado = models.BooleanField(default=True, verbose_name='¿Activo?')

    # Informacion fiscal 
    rfc = models.CharField(max_length=13)
    homoclave = models.CharField(max_length=3, blank=True, null=True)
    constancia_fiscal = models.FileField(upload_to='constancias_fiscales/', blank=True, null=True)

    class Meta:
        verbose_name = ("Contribuyente")
        verbose_name_plural = ("Contribuyentes")

    def __str__(self):
        if self.tipoPersona == 'PF':
            # Persona Física: usar nombre y apellidos
            nombre_completo = f"{self.nombre} ".strip()
        else:
            # Persona Moral: usar la razón social
            nombre_completo = self.razonSocial
        return f"{self.rfc} - {nombre_completo}"

    def save(self, *args, **kwargs):
        # Convertir todos los campos CharField y TextField a mayúsculas antes de guardar, excepto email
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)) and field.name != 'email':
                value = getattr(self, field.name)
                if value:
                    setattr(self, field.name, value.upper())

        try:
            this = Contribuyente.objects.get(id=self.id)
            if this.constancia_fiscal != self.constancia_fiscal:
                this.constancia_fiscal.delete(save=False)
        except Contribuyente.DoesNotExist:
            pass  # Es un nuevo objeto, por lo que no hay archivo anterior que eliminar

        super(Contribuyente, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.constancia_fiscal.delete(save=False)
        super(Contribuyente, self).delete(*args, **kwargs)

    def get_full_address(self):
        # Componentes de la dirección
        address_parts = []
        
        # Agregar calle y números si están disponibles
        if self.calle and self.calle.nombre:
            address_parts.append(self.calle.nombre)
        if self.numeroE:
            address_parts.append(f"Ext. {self.numeroE}")
        if self.numeroI:
            address_parts.append(f"Int. {self.numeroI}")

        # Agregar colonia
        if self.colonia and self.colonia.nombre:
            address_parts.append(self.colonia.nombre)
        
        # Agregar municipio
        if self.municipio and self.municipio.nombre:
            address_parts.append(self.municipio.nombre)
        
        # Unir las partes con comas y manejar los espacios correctamente
        full_address = ', '.join(part for part in address_parts if part)

        return full_address