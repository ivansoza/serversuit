from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.conf import settings
from catalogos.models import PersonalizacionTema, ServicioMunicipio, areasMunicipio
from weasyprint import HTML
from typing import Any
from django.views.decorators.http import require_GET
from contribuyente.models import Contribuyente
from django.http import JsonResponse
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib import messages
from agua.models import noServicio
from predio.models import predio
from .models import estadoNoServicio, estadoPredio
from .forms import estadoNoServicioForms, estadoPredioForms
from django.urls import reverse
import datetime
from django.db.models import Exists, OuterRef

class cobroSAgua(TemplateView):
    template_name = 'cobroSAgua.html'



class HomeOrdenesPago(TemplateView):
    template_name = 'home_odp.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('index')

        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': url_configuracion},
            'child': {'name': 'Inicio Ordenes de Pago', 'url': '/ordenesPago/home/'}
        }
        context['sidebar'] = 'ordenpago'

        return context
    
class CreateOrdenPago(TemplateView):
    template_name = 'ordendepago.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('home_odp')

        context["breadcrumb"] = {
            'parent': {'name': 'Inicio Ordenes de Pago', 'url': url_configuracion},
            'child': {'name': 'Crear Orden de Pago', 'url': '/ordenesPago/home/'}
        }
        context['sidebar'] = 'ordenpago'

        return context


class GenerarPDF(View):
    def get(self, request, *args, **kwargs):
        #El usuario debe estar autenticado y tiene un municipio asociado
        municipio_usuario = request.user.Municipio

        try:
            personalizacion_tema = PersonalizacionTema.objects.get(municipio=municipio_usuario)
           
            logotipo_url = f'{settings.BASE_URL}{personalizacion_tema.logotipo.url}'
        except ObjectDoesNotExist:
            logotipo_url = None
        # Contexto para la plantilla HTML
        contexto = {
            'logo': logotipo_url
        }

        # Renderizar la plantilla HTML con contexto
        html_string = render_to_string('tickets/tk_odp.html', contexto)

        # Convertir el HTML en un objeto WeasyPrint HTML
        html = HTML(string=html_string)

        # Generar el PDF
        pdf = html.write_pdf()

        # Crear una respuesta HTTP con el PDF generado
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mi_documento.pdf"'

class BAdeudos(TemplateView):
    template_name='busquedaAdeudo.html'
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Ordenes de pago', 'url': '/ordenesPago/home/'},
            'child': {'name': 'Adeudos', 'url': '/busqueda_adeudo/'}
        }
        return context
    

def buscar_contribuyente_deuda(request):
    query = request.GET.get('query', '')
    
    if query.isdigit():
        # Búsqueda por ID
        contribuyente = get_object_or_404(Contribuyente, id=query)
        nombre_completo = (
            f"{contribuyente.nombre} {contribuyente.apellidoP} {contribuyente.apellidoM}"
            if contribuyente.tipoPersona == Contribuyente.PERSONA_FISICA
            else contribuyente.razonSocial
        )
        if contribuyente.mc:
            nombre_completo += f" Y {contribuyente.nombre_mc} {contribuyente.apellidoP_mc} {contribuyente.apellidoM_mc}"
        
        # Obtener registros asociados
        predios = predio.objects.filter(contribuyente=contribuyente)
        servicios = noServicio.objects.filter(contri=contribuyente)
        
        # Prepara los datos de predios
        predio_data = [{
            'id': predio.id,
            'no_servicio': predio.clave_catastral,
            'tipo_servicio': predio.colonia.nombre,  # Asumiendo que tipo_servicio tiene un campo nombre
            'fecha_alta': predio.calle.nombre,
            'clave_catastral': predio.uso_predio,
            'contribuyente': predio.valor_catastral,
        } for predio in predios]

        # Prepara los datos de servicios
        servicio_data = [{
            'id': servicio.id,
            'no_servicio': servicio.noServicio,
            'tipo_servicio': servicio.tipoServicio.tipoServicio,  # Asumiendo que tipo_servicio tiene un campo nombre
            'fecha_alta': servicio.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            'contribuyente': nombre_completo
        } for servicio in servicios]

        # Combina los datos en una sola respuesta
        data = {
            'nombre_completo': nombre_completo,
            'email': contribuyente.email,
            'telefono': contribuyente.telefono,
            'direccion': f"{contribuyente.calle}, {contribuyente.numeroE}, {contribuyente.colonia}, {contribuyente.municipio}",
            'rfc': f"{contribuyente.rfc}{contribuyente.homoclave}",
            'predios': predio_data,
            'servicios': servicio_data
        }
        return JsonResponse(data)
    
    # Búsqueda por otros parámetros
    contribuyentes = Contribuyente.objects.filter(
        nombre__icontains=query
    ) | Contribuyente.objects.filter(
        apellidoP__icontains=query
    ) | Contribuyente.objects.filter(
        apellidoM__icontains=query
    ) | Contribuyente.objects.filter(
        rfc__icontains=query
    ) | Contribuyente.objects.filter(
        curp__icontains=query
    ) | Contribuyente.objects.filter(
        razonSocial__icontains=query
    )

    if contribuyentes.exists():
        if contribuyentes.count() > 1:
            # Si hay más de un contribuyente, devolver todos los resultados
            data = []
            for contribuyente in contribuyentes:
                if contribuyente.tipoPersona == Contribuyente.PERSONA_FISICA:
                    nombre_completo = f"{contribuyente.nombre} {contribuyente.apellidoP} {contribuyente.apellidoM}"
                    if contribuyente.mc:
                        nombre_completo += f" Y {contribuyente.nombre_mc} {contribuyente.apellidoP_mc} {contribuyente.apellidoM_mc}"
                else:
                    nombre_completo = contribuyente.razonSocial

                data.append({
                    'id': contribuyente.id,
                    'nombre_completo': nombre_completo,
                    'email': contribuyente.email,
                    'telefono': contribuyente.telefono,
                    'direccion': f"{contribuyente.calle}, {contribuyente.numeroE}, {contribuyente.colonia}, {contribuyente.municipio}",
                    'rfc': f"{contribuyente.rfc}{contribuyente.homoclave}"
                })
            return JsonResponse({'contribuyentes': data})
        else:
            # Si solo hay un contribuyente, devolver el único resultado
            contribuyente = contribuyentes.first()
            if contribuyente.tipoPersona == Contribuyente.PERSONA_FISICA:
                nombre_completo = f"{contribuyente.nombre} {contribuyente.apellidoP} {contribuyente.apellidoM}"
                if contribuyente.mc:
                    nombre_completo += f" Y {contribuyente.nombre_mc} {contribuyente.apellidoP_mc} {contribuyente.apellidoM_mc}"
            else:
                nombre_completo = contribuyente.razonSocial
            
            # Obtener registros asociados
            predios = predio.objects.filter(contribuyente=contribuyente)
            servicios = noServicio.objects.filter(contri=contribuyente)
            
            # Prepara los datos de predios
            predio_data = [{
                'id': predio.id,
                'clave_catastral': predio.clave_catastral,
                'colonia': predio.colonia.nombre,  # Asumiendo que tipo_servicio tiene un campo nombre
                'calle': predio.calle.nombre,
                'uso_predio': predio.uso_predio,
                'calor_catastral': predio.valor_catastral,
            } for predio in predios]

            # Prepara los datos de servicios
            servicio_data = [{
                 'id': servicio.id,
                'no_servicio': servicio.noServicio,
                'tipo_servicio': servicio.tipoServicio.tipoServicio,  # Asumiendo que tipo_servicio tiene un campo nombre
                'fecha_alta': servicio.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
                'contribuyente': nombre_completo
            } for servicio in servicios]

            data = {
                'nombre_completo': nombre_completo,
                'email': contribuyente.email,
                'telefono': contribuyente.telefono,
                'direccion': f"{contribuyente.calle}, {contribuyente.numeroE}, {contribuyente.colonia}, {contribuyente.municipio}",
                'rfc': f"{contribuyente.rfc}{contribuyente.homoclave}",
                'predios': predio_data,
                'servicios': servicio_data
            }
            return JsonResponse(data)
    else:
        # Agregar mensaje de error y redirigir
        return JsonResponse({'error': 'No se encontraron resultados'}, status=404)
    

class tablaDeuda(TemplateView):
    template_name = 'tablaAdeudo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contribuyente_id = self.request.GET.get('id')
        entity_type = self.request.GET.get('type')

        if not contribuyente_id or not entity_type:
            context['error'] = 'Faltan parámetros para mostrar los datos.'
            return context

        if entity_type == 'predio':
            predio_instance = get_object_or_404(predio, id=contribuyente_id)
            tipo_display = predio_instance.get_uso_predio_display()
            context['tipo_display'] = tipo_display
            context['predio'] = predio_instance
            initial_no_predio = predio_instance.id
            context['formP'] = estadoPredioForms(initial={'claveCatastarl': initial_no_predio})
            context['servicios'] = noServicio.objects.filter(id=contribuyente_id)
            adeudosP = estadoPredio.objects.filter(claveCatastarl=predio_instance)
            años_utilizados = set(adeudosP.values_list('anio', flat=True))
            años_disponibles = [year for year in range(1990, datetime.datetime.now().year + 1) if year not in años_utilizados]

            # Ordenar los años en orden descendente
            años_disponibles.sort(reverse=True)

            context['años_disponibles'] = años_disponibles
            context['adeudosP'] = adeudosP
            total_monto2 = sum(adP.monto for adP in adeudosP)
            context['total_monto2'] = total_monto2
        elif entity_type == 'servicio':
            servicio_instance = get_object_or_404(noServicio, id=contribuyente_id)
            context['servicio'] = servicio_instance
            context['predios'] = predio.objects.filter(id=contribuyente_id)
            initial_no_servicio = servicio_instance.id
            context['form'] = estadoNoServicioForms(initial={'noServicio': initial_no_servicio})
            context['meses'] = list(range(1, 13))

            # Consulta los registros de estadoNoServicio para el número de servicio dado
            adeudos = estadoNoServicio.objects.filter(noServicio=servicio_instance)
            # Obtener los años ya utilizados para el número de servicio
            años_utilizados = set(adeudos.values_list('anio', flat=True))
            años_disponibles = [year for year in range(1990, datetime.datetime.now().year + 1) if year not in años_utilizados]
            años_disponibles.sort(reverse=True)

            context['años_disponibles'] = años_disponibles

            # Calcula la suma de los montos
            total_monto = sum(adeudo.monto for adeudo in adeudos)
            context['total_monto'] = total_monto
            
            # Agrupa los registros por año
            grouped_adeudos = {}
            for adeudo in adeudos:
                year = adeudo.anio
                if year not in grouped_adeudos:
                    grouped_adeudos[year] = {'adeudos': [], 'total_monto': 0}
                grouped_adeudos[year]['adeudos'].append(adeudo)
                grouped_adeudos[year]['total_monto'] += adeudo.monto
            
            # Calcula la suma de los montos totales
            total_monto = sum(adeudo.monto for adeudo in adeudos)
            context['total_monto'] = total_monto
            
            context['grouped_adeudos'] = grouped_adeudos
        else:
            context['error'] = 'Tipo de entidad no válido.'
        context['breadcrumb'] = {
            'parent': {'name': 'Búsqueda de contribuyente', 'url': '/ordenesPago/busqueda_adeudo/'},
            'child': {'name': 'Información de pagos', 'url': '/busqueda_adeudo/'}
        }
        return context

def guardar_registros(no_servicio_id, anio, monto, meses):
    for mes in meses:
        if mes:
            estadoNoServicio.objects.create(
                noServicio=get_object_or_404(noServicio, id=no_servicio_id),
                anio=anio,
                mes=int(mes),
                monto=monto
            )

def info_adeudo2(request):
    if request.method == 'POST':
        no_servicio_id = request.POST.get('noServicio')
        anio = request.POST.get('anio')
        monto = request.POST.get('monto')
        meses = request.POST.get('meses', '').split(',')
        # Guardar los registros
        try:
            guardar_registros(no_servicio_id, anio, monto, meses)
            messages.success(request, 'El registro se ha guardado correctamente.')

            return JsonResponse({
                'status': 'success',
                'id': no_servicio_id,
                'type': 'servicio',  # Ajusta este valor según el tipo de entidad que estás manejando
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})
    else:
        return JsonResponse({'status': 'error', 'error': 'Método no permitido'})

def guardar_registros_predio(claveCatastarl_id, anio, monto):
            estadoPredio.objects.create(
                claveCatastarl=get_object_or_404(predio, id=claveCatastarl_id),
                anio=anio,
                monto=monto
            )

def info_adeudo_predio(request):
    if request.method == 'POST':
        claveCatastral_id = request.POST.get('claveCatastarl')
        anio = request.POST.get('anio')
        monto = request.POST.get('monto')
 
        try:
            guardar_registros_predio(claveCatastral_id, anio, monto)
            messages.success(request, 'El registro se ha guardado correctamente.')

            return JsonResponse({
                'status': 'success',
                'id': claveCatastral_id,
                'type': 'predio',  # Ajusta este valor según el tipo de entidad que estás manejando
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})
    else:
        return JsonResponse({'status': 'error', 'error': 'Método no permitido'})



def get_areas(request):
    if request.user.is_authenticated:
        if not request.user.Municipio:
            return JsonResponse({'error': 'Usuario no tiene un municipio asignado.'}, status=400)

        # Obtener las áreas asignadas al usuario que están asociadas al municipio del usuario
        areas_usuario = request.user.areas.all()
        if not areas_usuario.exists():
            return JsonResponse({'error': 'No se le ha asignado ninguna área al usuario.'}, status=404)

        # Consultar todas las áreas del municipio que coinciden con las áreas del usuario
        areas_municipio = areasMunicipio.objects.filter(
            municipio=request.user.Municipio,
            area__in=areas_usuario
        ).first()

        if areas_municipio:
            # Obtener todos los servicios activos para esas áreas en el municipio
            servicios = ServicioMunicipio.objects.filter(
                municipio=request.user.Municipio,
                area__in=areas_municipio.area.all()
            ).values_list('area', flat=True).distinct()

            # Filtrar las áreas del usuario que tienen al menos un servicio
            areas_con_servicio = areas_usuario.filter(id__in=servicios)

            if areas_con_servicio.exists():
                data = [{'id': area.id, 'nombre': area.Area} for area in areas_con_servicio]
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse({'error': 'No hay ningún servicio agregado a las áreas asignadas al usuario.'}, status=404)
        else:
            return JsonResponse({'error': 'No hay áreas disponibles para el municipio asignado.'}, status=404)

    else:
        return JsonResponse({'error': 'Acceso no autorizado.'}, status=403)

def get_servicios_por_area(request, area_id):
    if request.user.is_authenticated and request.user.Municipio:
        servicios = ServicioMunicipio.objects.filter(
            municipio=request.user.Municipio, 
            area_id=area_id
        ).distinct()

        if servicios.exists():
            data = [{'id': servicio.id, 'nombre': servicio.concepto, 'monto': str(servicio.monto)} for servicio in servicios]
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'No hay servicios disponibles para esta área.'}, status=404)
    else:
        return JsonResponse({'error': 'Usuario no autenticado o sin municipio asignado.'}, status=403)