from django.contrib import admin

# Register your models here.

from op.models import ODP,tipoDocumento,Atendido,RevisionPropuesta

# Register your models here.
admin.site.register(ODP)
admin.site.register(tipoDocumento)
admin.site.register(Atendido)
admin.site.register(RevisionPropuesta)

