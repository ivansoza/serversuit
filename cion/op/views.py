# En tu archivo views.py

from http.client import HTTPResponse
from django.views.generic import ListView
from venv import logger
from django.views.generic import TemplateView

from catalogos.models import areasMunicipio
from .forms import ODPForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, UpdateView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import AtendidoForm
from .models import ODP, RevisionPropuesta, areas,Atendido
from django.utils import timezone
from datetime import timedelta
class op(TemplateView):
    template_name = 'aplications/ODP/componentes/homeop.html'
    form_class = ODPForm
    success_url = reverse_lazy('lista_odp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'op'
        context['form'] = self.form_class(user=self.request.user, prefix='oficialia_de_partes')  # Pasar el usuario al formulario
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard'},
            'child': {'name': 'Nuevo Registro', 'url': '/oficialia_de_partes/'}
        }
        return context

    logger = logging.getLogger(__name__)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, user=request.user, prefix='oficialia_de_partes')  # Pasar el usuario al formulario
        if form.is_valid():
            form_instance = form.save(commit=False)
            logger.info(f"Datos del formulario a guardar: {form.cleaned_data}")
            form_instance.save()
            messages.success(request, 'El registro se ha guardado correctamente.')
            return HttpResponseRedirect(self.success_url)
        else:
            logger.error(f"Formulario inválido: {form.errors}")
            return self.render_to_response(self.get_context_data(form=form))




class tablaOP(TemplateView):
    template_name = 'aplications/ODP/componentes/tabla.html'
    form_class = ODPForm
    success_url = reverse_lazy('tablaOP')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user

        # Obtener el municipio del usuario
        municipio = getattr(usuario, 'Municipio', None)

        # Inicializar registros
        registros_por_area = {}
        hay_nuevos_registros = False

        if municipio:
            # Obtener las áreas asociadas al municipio del usuario
            areas_municipio = areasMunicipio.objects.filter(municipio=municipio)
            areas_visibles = areas.objects.filter(id__in=areas_municipio.values('area'))

            # Filtrar áreas asignadas al usuario
            if usuario.areas.exists():
                areas_visibles = areas_visibles.filter(id__in=usuario.areas.values('id'))
            else:
                areas_visibles = areas.objects.none()
        else:
            areas_visibles = areas.objects.none()

        for area in areas_visibles:
            registros = ODP.objects.filter(areas=area)
            for odp in registros:
                odp.tiempo_restante = odp.get_tiempo_restante()
                odp.tiene_revision = RevisionPropuesta.objects.filter(propuesta__odp=odp).exists()  # Verificar si tiene una revisión

                if not odp.tiene_revision:
                    hay_nuevos_registros = True

            registros_por_area[area.Area] = registros

        context['registros_por_area'] = registros_por_area
        context['form'] = self.form_class(prefix='oficialia_de_partes')
        context['breadcrumb'] = {
            'parent': {'name': 'Registros por atender'},
        }
        context['hay_nuevos_registros'] = hay_nuevos_registros

        return context

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk')
        if pk:
            odp = get_object_or_404(ODP, pk=pk)
            odp.delete()
            messages.success(self.request, 'Registro eliminado correctamente.')
        return redirect('tablaOP')




class EditarODPView(UpdateView):
    model = ODP
    form_class = ODPForm
    template_name = 'aplications/ODP/componentes/editar_odp.html'
    success_url = reverse_lazy('lista_odp')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Registro actualizado correctamente.')
        return super().form_valid(form)


def obtener_formulario_edicion(request, pk):
    odp = get_object_or_404(ODP, pk=pk)
    form = ODPForm(request.POST or None, request.FILES or None, instance=odp, user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # Puedes agregar lógica adicional después de guardar el formulario
            return redirect('lista_odp')
    return render(request, 'aplications/ODP/componentes/odp_form.html', {'form': form})


def eliminar_odp(request, pk):
    odp = get_object_or_404(ODP, pk=pk)
    
    if request.method == 'POST':
        odp.delete()
        messages.success(request, 'Registro eliminado correctamente')  # Mensaje de éxito
        return redirect('lista_odp')  # Redirige a la página principal de la tabla después de eliminar
        
    return render(request, 'eliminar_odp.html', {'odp': odp})




def atender_odp(request, odp_id):
    odp = get_object_or_404(ODP, id=odp_id)
    
    if request.method == 'POST':
        form = AtendidoForm(request.POST, request.FILES)  # Agregar request.FILES
        if form.is_valid():
            atendido = form.save(commit=False)
            atendido.odp = odp
            atendido.save()
            return redirect('tablaOP')  # Reemplazar con la URL correcta
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    form = AtendidoForm()
    return render(request, 'atender_form.html', {'form': form, 'odp': odp})



class AtendidosListView(TemplateView):
    template_name = 'aplications/ODP/componentes/atendidos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todos los registros atendidos
        atendidos = Atendido.objects.select_related('odp').all()
        
        # Obtener las revisiones propuestas relacionadas
        for atendido in atendidos:
            revision = RevisionPropuesta.objects.filter(propuesta=atendido).first()
            atendido.revision = revision

        context['atendidos'] = atendidos
        context['navbar'] = 'op'
        context['breadcrumb'] = {
            'parent': {'name': 'Registros atendidos'},
        }
        return context

    



class ODPListView(ListView):
    model = ODP
    template_name = 'aplications/ODP/componentes/tablageneralodp.html'
    context_object_name = 'registros'

    # Configuración del logger
    logger = logging.getLogger(__name__)

    def get_queryset(self):
        # Aquí puedes personalizar la consulta si es necesario
        return ODP.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'op'
        context['breadcrumb'] = {
            'parent': {'name': 'Nuevo Registro', 'url': '/op/op'},
            'child': {'name': 'Registros Oficialia'}
        }
        
        # Añadir tiempos restantes al contexto
        registros = context['registros']
        for registro in registros:
            registro.tiempo_restante = registro.get_tiempo_restante()
        
        return context
    
    
from django.views.generic import ListView
from .models import Atendido, RevisionPropuesta

class AtendidoListView(ListView):
    model = Atendido
    template_name = 'revisionpropuesta_list.html'
    context_object_name = 'atendidos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        atendidos = context['atendidos']
        for atendido in atendidos:
            atendido.revision = RevisionPropuesta.objects.filter(propuesta=atendido).first()
        return context

 
 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Atendido, RevisionPropuesta
from .forms import RevisionPropuestaForm  # Si tienes un formulario específico

def guardar_revision_propuesta(request, atendido_id):
    atendido = get_object_or_404(Atendido, id=atendido_id)
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        acepta = request.POST.get('acepta') == 'on'
        noacepta = request.POST.get('noacepta') == 'on'
        observaciones = request.POST.get('observaciones')
        
        # Verificar si ya existe un registro para este `Atendido`
        revision, created = RevisionPropuesta.objects.get_or_create(
            propuesta=atendido,
            defaults={
                'fecha': fecha,
                'hora': hora,
                'acepta': acepta,
                'noacepta': noacepta,
                'observaciones': observaciones
            }
        )
        if not created:
            # Actualizar los campos si ya existe
            revision.fecha = fecha
            revision.hora = hora
            revision.acepta = acepta
            revision.noacepta = noacepta
            revision.observaciones = observaciones
            revision.save()
            
        return redirect('revision_list')  # Redirige a donde quieras después de guardar
    
    # Manejo de GET o errores
    return redirect('tu_url_de_lista')