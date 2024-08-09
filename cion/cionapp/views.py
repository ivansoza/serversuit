from django.shortcuts import render
from .models import PaginaInicio
from catalogos.models import PersonalizacionTema
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist



@login_required
def index(request):
    municipio_usuario = request.user.Municipio  

    pagina_inicio = PaginaInicio.objects.filter(municipio=municipio_usuario).first()

    fondo_url = pagina_inicio.imagen_inicio.url if pagina_inicio and pagina_inicio.imagen_inicio else None

    context = {
        'pagina_inicio': pagina_inicio,
        'fondo_url': fondo_url
    }

    return render(request, 'general/index.html', context)