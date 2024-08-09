from django.db import models
from agua.models import noServicio
from catalogos.models import ServicioMunicipio, areas
from contribuyente.models import Contribuyente
from usuarios.models import CustomUser
from predio.models import predio
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_year(value):
    if value < 1900 or value > 2100:
        raise ValidationError(
            _('El año debe estar entre 1900 y 2100.'),
            params={'value': value},
        )

def validate_month(value):
    if value < 1 or value > 12:
        raise ValidationError(
            _('El mes debe estar entre 1 y 12.'),
            params={'value': value},
        )
    
class estadoNoServicio(models.Model):
    noServicio = models.ForeignKey(noServicio, on_delete=models.CASCADE, verbose_name='Numero de servicio de agua potable')
    anio = models.IntegerField(validators=[validate_year], verbose_name='Año')
    mes = models.IntegerField(validators=[validate_month], verbose_name='Mes')
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto', blank=True, null=True)
    pagado = models.BooleanField(default=False, verbose_name='¿El adeudo a sido pagado?')

    def __str__(self):
        return f"{self.noServicio} - {self.anio}-{self.mes}"



class estadoPredio(models.Model):
    claveCatastarl = models.ForeignKey(predio, on_delete=models.CASCADE, verbose_name='Clave catastral')
    anio = models.IntegerField(validators=[validate_year], verbose_name='Año')
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto', blank=True, null=True)
    pagado = models.BooleanField(default=False, verbose_name='¿El adeudo a sido pagado?')
    def __str__(self):
        return f"{self.claveCatastarl} - {self.anio}"

class statusServicio(models.Model):
    noServicio = models.ForeignKey(noServicio, on_delete=models.CASCADE, verbose_name='No. de servicio')
    anio = models.CharField(max_length=4, verbose_name='Año')
    enero = models.BooleanField(default=False, verbose_name='Enero')
    febrero = models.BooleanField(default=False, verbose_name='Febrero')
    marzo = models.BooleanField(default=False, verbose_name='Marzo')
    abril = models.BooleanField(default=False, verbose_name='Abril')
    mayo = models.BooleanField(default=False, verbose_name='Mayo')
    junio = models.BooleanField(default=False, verbose_name='Junio')
    julio = models.BooleanField(default=False, verbose_name='Julio')
    agosto = models.BooleanField(default=False, verbose_name='Agosto')
    septiembre = models.BooleanField(default=False, verbose_name='Septiembre')
    octubre = models.BooleanField(default=False, verbose_name='Octubre')
    noviembre = models.BooleanField(default=False, verbose_name='Noviembre')
    diciembre = models.BooleanField(default=False, verbose_name='Diciembre')

class EstatusPredio(models.Model):
    predio = models.ForeignKey(predio, on_delete=models.CASCADE, verbose_name="Predio relacionado")
    ano = models.IntegerField(verbose_name="Año")
    pagado = models.BooleanField(default=False, verbose_name="Pagado")

    class Meta:
        verbose_name = "Estado de Predio"
        verbose_name_plural = "Estados de Predios"
        unique_together = (('predio', 'ano'),)  # Asegura que no hay duplicados para el mismo año y predio

    def _str_(self):
        estado_pago = "Pagado" if self.pagado else "No Pagado"
        return f"{self.predio.clave_catastral} - {self.ano} - {estado_pago}"



class ordenesPago(models.Model):
    # Campos Generales
    folio = models.CharField(max_length=12, verbose_name='Folio')
    area = models.ForeignKey(areas, on_delete=models.CASCADE, verbose_name='Área')  
    fecha_expedicion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de expedición')
    contribuyente = models.ForeignKey(Contribuyente, on_delete=models.CASCADE, verbose_name='Contribuyente', null=True, blank=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Usuario')
    ESTADO_PAGO = [
        ('POR PAGAR','POR PAGAR'),
        ('PAGADO','PAGADO'),
    ]
    estado = models.CharField(max_length=10, verbose_name='Estado de la orden de pago',choices=ESTADO_PAGO, default='POR PAGAR')
    observaciones = models.TextField(verbose_name='Observaciones', blank=True, null=True)
    total_descuento = models.DecimalField(max_digits=10,decimal_places=2, verbose_name='Total descuentos', blank=True, null=True)
    total_Recargos = models.DecimalField(max_digits=10,decimal_places=2, verbose_name='Total descuentos', blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10,decimal_places=2, verbose_name='Subtotal', blank=True, null=True)
    total = models.DecimalField(max_digits=10,decimal_places=2, verbose_name='Total')
    def __str__(self):
        return f"Orden de Pago {self.folio} - {self.contribuyente}"
    
class detalleOrdenPago(models.Model):
    folioOrden = models.ForeignKey(ordenesPago, on_delete=models.CASCADE, verbose_name='Folio de orden de pago')
    area = models.ForeignKey(areas, on_delete=models.CASCADE, verbose_name='Área')  

    conceptos = models.ForeignKey(ServicioMunicipio, on_delete=models.CASCADE, verbose_name='Concepto de pago')
    sub_total = models.DecimalField(max_digits=10,decimal_places=2, verbose_name='Subtotal', blank=True, null=True)
    fecha_detalle = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    # Campos Agua
    noServicio = models.ForeignKey(noServicio, on_delete=models.CASCADE, verbose_name='No. de servicio', null=True, blank=True)
    sServicio = models.ForeignKey(statusServicio, on_delete=models.CASCADE, verbose_name='Estatus del No. servicio', null=True, blank=True)
    enero = models.BooleanField(default=False, verbose_name='Enero')
    febrero = models.BooleanField(default=False, verbose_name='Febrero')
    marzo = models.BooleanField(default=False, verbose_name='Marzo')
    abril = models.BooleanField(default=False, verbose_name='Abril')
    mayo = models.BooleanField(default=False, verbose_name='Mayo')
    junio = models.BooleanField(default=False, verbose_name='Junio')
    julio = models.BooleanField(default=False, verbose_name='Julio')
    agosto = models.BooleanField(default=False, verbose_name='Agosto')
    septiembre = models.BooleanField(default=False, verbose_name='Septiembre')
    octubre = models.BooleanField(default=False, verbose_name='Octubre')
    noviembre = models.BooleanField(default=False, verbose_name='Noviembre')
    diciembre = models.BooleanField(default=False, verbose_name='Diciembre')
    
    # Campos Predio
    claveCatastral = models.ForeignKey(predio, on_delete=models.CASCADE, verbose_name='Clave catastral', null=True, blank=True)
    statusPredio = models.ForeignKey(EstatusPredio, on_delete=models.CASCADE, verbose_name='Estatus del predio',null=True, blank=True)

    def __str__(self):
        return f"Orden de Pago {self.folioOrden} - {self.conceptos.concepto}"
    