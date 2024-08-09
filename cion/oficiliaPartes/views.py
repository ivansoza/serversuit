from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from .forms import recepcionDocumentosForms, respuestaForms
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import recepcionDocumentos, respuesta
from django.shortcuts import redirect
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.

class homeOdp(TemplateView):
    template_name='inicio_ODP.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Oficialia de partes'}
        }
        return context

class tablaregistrosDocsODP(TemplateView):
    template_name='tabladeODP.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['odp'] = recepcionDocumentos.objects.filter(atendido=False)
        context['breadcrumb'] = {
            'parent': {'name': 'Oficialia de partes', 'url': '/oficialiaPartes/inicioODP'},
            'child': {'name': 'Registro de documentación'}
        }
        return context
    
class formRegistrosDocsODP(TemplateView):
    template_name = 'form_ODP.html'
    form_class = recepcionDocumentosForms
    success_url = reverse_lazy('registrosODP')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el municipio del usuario logueado
        usuario = self.request.user
        nombre_usuario = usuario.first_name
        apellido_usuario = usuario.last_name
        apellido_materno = usuario.apellido_materno
        municipio = usuario.Municipio.numero_municipio  # Ajusta esto según el nombre correcto del campo en tu modelo
        context['form'] = self.form_class(municipio=municipio, initial={
            'recibio': f'{nombre_usuario} {apellido_usuario} {apellido_materno}'
        })
        context['breadcrumb'] = {
            'parent': {'name': 'Registro de documentación', 'url': '/oficialiaPartes/registrosODP'},
            'child': {'name': 'Formulario de documentación'}
        }
        return context

    def post(self, request, *args, **kwargs):
        # Obtén el municipio del usuario logueado
        municipio = request.user.Municipio.numero_municipio  # Ajusta esto según el nombre correcto del campo en tu modelo
        
        # Inicializa el formulario con los datos del POST y el municipio
        form = self.form_class(request.POST, request.FILES, municipio=municipio)

        if form.is_valid():
            # Si el número de servicio no existe, guarda el formulario
            form_instance = form.save(commit=False)
            form_instance.save(municipio=municipio)
            messages.success(request, 'El registro se ha guardado correctamente.')
            return HttpResponseRedirect(self.success_url)
        else:
            messages.error(request, 'Error al enviar el formulario, por favor revise los datos.')
            # Renderizar la plantilla con el formulario y los mensajes
            return self.render_to_response(self.get_context_data(form=form))
        
class EditarRegistroView(UpdateView):
    model = recepcionDocumentos
    form_class = recepcionDocumentosForms
    template_name = 'form_ODP.html'
    success_url = reverse_lazy('registrosODP')  # Redirige a la página de registros después de guardar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Incluye el breadcrumb y cualquier otra información necesaria en el contexto
        context['breadcrumb'] = {
            'parent': {'name': 'Registro de documentación', 'url': '/oficialiaPartes/registrosODP'},
            'child': {'name': 'Editar registro'}
        }
        return context

    def form_valid(self, form):
        # Llama al método de la clase base para guardar el formulario
        response = super().form_valid(form)
        
        # Añade el mensaje de éxito
        messages.success(self.request, 'El registro se ha guardado correctamente.')
        
        return response
    
class tablasAreas(TemplateView):
    template_name = 'tablasAreas.html'
    form_class = respuestaForms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        filtro = self.request.GET.get('filtro', 'todos')  # Obtener el filtro de la URL

        # Obtener los IDs de todas las áreas relacionadas
        areas = usuario.areas.all()
        area_ids = areas.values_list('id', flat=True)

        # Filtrar documentos según el filtro activo
        if filtro == 'sin_respuesta':
            context['odp'] = recepcionDocumentos.objects.filter(areas__id__in=area_ids).exclude(id__in=respuesta.objects.values_list('odp_id', flat=True))
        elif filtro == 'con_respuesta':
            context['odp'] = recepcionDocumentos.objects.filter(areas__id__in=area_ids, id__in=respuesta.objects.values_list('odp_id', flat=True))

        else:
            context['odp'] = recepcionDocumentos.objects.filter(areas__id__in=area_ids)

        # Agregar el filtro activo al contexto
        context['filtro_activo'] = filtro

        area_names = ', '.join([area.Area for area in areas])
        context['breadcrumb'] = {
            'parent': {'name': 'Registro de documentación', 'url': '/oficialiaPartes/registrosODP'},
            'child': {'name': 'Oficialía de partes área: ' + area_names}
        }
        nombre_usuario = usuario.first_name
        apellido_usuario = usuario.last_name
        apellido_materno = usuario.apellido_materno
        context['form'] = self.form_class(initial={'usuario': f'{nombre_usuario} {apellido_usuario} {apellido_materno}'})
        return context


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            respuesta_instance = form.save()
            recepcion_doc = respuesta_instance.odp
            recepcion_doc.atendido = True
            recepcion_doc.save()
            messages.success(self.request, 'El registro se ha guardado correctamente.')
            return redirect('areasODP')
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

def document_info(request, id):
    documento = get_object_or_404(recepcionDocumentos, id=id)
    data = {
        'folio': documento.folio_odp,
        'tipo_doc': documento.tipo_doc.nombre,
        'prioridad': documento.prioridad,
        'dependencia': documento.dependencia,
        'procedencia': documento.procedencia,
        'archivo': documento.archivo.url if documento.archivo else None,
        'observaciones': documento.observaciones,
        'fecha_creacion': documento.fecha_creacion,
    }
    return JsonResponse(data)