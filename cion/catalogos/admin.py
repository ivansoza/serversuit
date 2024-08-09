from django.contrib import admin

from catalogos.models import Estado,Municipio,areas,Autoridad, PersonalizacionTema,areas,Autoridad, tipoServicioAgua, Servicios, Descuentos,Recargos, ServicioMunicipio, areasMunicipio, Colonia, Calle
from django import forms

# Register your models here.
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('numero_estado', 'nombre')  # Mostrar número y nombre en la lista
    ordering = ('numero_estado',)  # Ordenar los estados por número de estado ascendente

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Municipio)
admin.site.register(Autoridad)
admin.site.register(tipoServicioAgua)
class ServiciosAdmin(admin.ModelAdmin):
    list_display = ('codigoServicio', 'descripcion')
    ordering = ('codigoServicio',)  # Asegura que el admin utilice este orden

admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(Descuentos)
admin.site.register(Recargos)
admin.site.register(ServicioMunicipio)
admin.site.register(Calle)
admin.site.register(Colonia)

admin.site.register(areasMunicipio)


@admin.register(PersonalizacionTema)
class PersonalizacionTemaAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'tipo_diseno', 'tipo_sidebar', 'tipo_icono_sidebar', 'color_1','color_1a', 'color_2','color_2a')
    list_filter = ('tipo_diseno', 'tipo_sidebar', 'tipo_icono_sidebar')
    search_fields = ('municipio__nombre',)
    ordering = ('municipio',)

    def get_municipio_nombre(self, obj):
        return obj.municipio.nombre
    get_municipio_nombre.short_description = 'Municipio'
    get_municipio_nombre.admin_order_field = 'municipio__nombre'






admin.site.register(areas)

