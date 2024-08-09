from django.contrib import admin
from .models import recepcionDocumentos, respuesta, tipoDocumento
# Register your models here.

admin.site.register(recepcionDocumentos)
admin.site.register(respuesta)
admin.site.register(tipoDocumento)