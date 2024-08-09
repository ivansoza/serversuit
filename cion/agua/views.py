from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from catalogos.models import areasMunicipio
from contribuyente.models import Contribuyente
from django.urls import reverse_lazy
from .forms import noServicioForm
from django.http import HttpResponseRedirect
from .models import noServicio
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from predio.models import predio
from datetime import datetime
import calendar
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Value, CharField
from django.db.models.functions import Concat

class homeAguaView(TemplateView):
    template_name = 'homeAgua.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Servicio de Agua Potable', 'url': '/homeAgua/'}
        }

        context['sidebar'] = 'homeagua'

        return context
    
class formularioAgua(LoginRequiredMixin, TemplateView):
    template_name = 'forms.html'
    form_class = noServicioForm
    success_url = reverse_lazy('registrosAgua')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Registros de No. servicio', 'url': '/agua/registrosAgua/'},
            'child': {'name': 'Formulario de registro de numero de servicio', 'url': '/formularioAgua/'}
        }
        # Establecer los valores iniciales aquí
        initial_data = {
            'municipio': self.request.user.Municipio,
            'registro': f"{self.request.user.first_name} {self.request.user.last_name}"
        }
        context['form'] = self.form_class(initial=initial_data)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            no_servicio = form.cleaned_data.get('noServicio')

            if noServicio.objects.filter(noServicio=no_servicio).exists():
                messages.error(request, 'El número de servicio ya está registrado.')
                # Renderizar la plantilla con el formulario y los mensajes
                return self.render_to_response(self.get_context_data(form=form))
            
            # Si el número de servicio no existe, guarda el formulario
            form_instance = form.save(commit=False)
            form_instance.save()
            messages.success(request, 'El registro se ha guardado correctamente.')
            return HttpResponseRedirect(self.success_url)
        else:
            messages.error(request, 'Error al enviar el formulario, por favor revise los datos.')
            # Renderizar la plantilla con el formulario y los mensajes
            return self.render_to_response(self.get_context_data(form=form))


        
def obtener_municipio_usuario(request):
    if request.user.is_authenticated:
        usuario = request.user
        municipio_usuario = usuario.Municipio  # Ajusta esto según tu modelo de Usuario
        return municipio_usuario
    return None 

class TablaRegistrosAgua(LoginRequiredMixin, ListView):
    model = noServicio
    template_name = 'registros.html'
    context_object_name = 'servicios'

    def get_queryset(self):
        queryset = super().get_queryset()
        municipio_usuario = obtener_municipio_usuario(self.request)
        if municipio_usuario:
            queryset = queryset.filter(municipio=municipio_usuario)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Servicio de Agua Potable', 'url': '/agua/homeAgua/'},
            'child': {'name': 'Registros de No. servicio', 'url': '/formularioAgua/'}
        }
        return context
        

@csrf_exempt
def eliminar_no_servicio(request, id):
    if request.method == 'DELETE':
        try:
            no_servicio = get_object_or_404(noServicio, id=id)
            municipio_usuario = obtener_municipio_usuario(request)
            
            if municipio_usuario:
                no_servicio_municipio = noServicio.objects.filter(municipio=municipio_usuario)
                no_servicio.delete()
                
                # Devolver la cantidad actualizada de registros filtrados
                count = no_servicio_municipio.count()
                return JsonResponse({'success': True, 'count': count})
            else:
                return JsonResponse({'success': False, 'error': 'Usuario sin municipio asignado'}, status=400)
        
        except noServicio.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Registro no encontrado'}, status=404)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

def buscar_contribuyente(request):
    consulta = request.GET.get('consulta', None)
    if consulta:
        # Filtrar por RFC si la consulta tiene exactamente 10 o 9 caracteres
        if len(consulta) == 9 or len(consulta) == 10:
            contribuyentes = Contribuyente.objects.filter(rfc__iexact=consulta)
        else:
            # Buscar por nombre completo y razón social simultáneamente
            contribuyentes = Contribuyente.objects.annotate(
                nombre_completo=Concat(
                    'nombre',
                    Value(' '),
                    'apellidoP',
                    Value(' '),
                    'apellidoM',
                    output_field=CharField(),
                )
            ).filter(
                Q(nombre_completo__icontains=consulta) | 
                Q(razonSocial__icontains=consulta)
            )

        if contribuyentes.exists():
            data = []
            for contribuyente in contribuyentes:
                contrib_data = {
                    'id': contribuyente.id,
                    'tipoPersona': contribuyente.tipoPersona,
                    'homoclave': contribuyente.homoclave,
                    'rfc': contribuyente.rfc.upper() if contribuyente.rfc else '',
                    'curp': contribuyente.curp.upper() if contribuyente.curp else '',
                    'nombre': contribuyente.nombre.upper() if contribuyente.nombre else '',
                    'ApellidoP': contribuyente.apellidoP.upper() if contribuyente.apellidoP else '',
                    'ApellidoM': contribuyente.apellidoM.upper() if contribuyente.apellidoM else '',
                    'razonSocial': contribuyente.razonSocial.upper() if contribuyente.razonSocial else '',
                    'email': contribuyente.email.upper() if contribuyente.email else '',
                    'telefono': contribuyente.telefono,
                    'mc': contribuyente.mc,
                    'nombre_mc': contribuyente.nombre_mc.upper() if contribuyente.nombre_mc else '',
                    'ApellidoP_mc': contribuyente.apellidoP_mc.upper() if contribuyente.apellidoP_mc else '',
                    'ApellidoM_mc': contribuyente.apellidoM_mc.upper() if contribuyente.apellidoM_mc else '',
                }
                data.append(contrib_data)
            return JsonResponse({'contribuyentes': data})
        else:
            return JsonResponse({'error': 'Contribuyente no encontrado.'}, status=404)
    else:
        return JsonResponse({'error': 'Consulta vacía.'}, status=400)


def buscar_predio(request):
    consulta = request.GET.get('consulta', '').strip()
    if consulta:
        # Filtrar por clave catastral si la consulta tiene una longitud específica
        if len(consulta) == 10:  # Asumiendo que la clave catastral tiene una longitud fija
            predios = predio.objects.filter(clave_catastral__iexact=consulta)
        else:
           predios = predio.objects.annotate(
                nombre_completo=Concat(
                    'nombre',
                    Value(' '),
                    'ApellidoP',
                    Value(' '),
                    'ApellidoM',
                    output_field=CharField(),
                )
            ).filter(
                Q(nombre_completo__icontains=consulta) | 
                Q(razonSocial__icontains=consulta)
            )

        if predios.exists():
            data = []
            for predio1 in predios:
                contribuyente = predio1.contribuyente
                contrib_data = {
                    'id': predio1.id,
                    'clave_catastral': predio1.clave_catastral,
                    'estado': predio1.estado,
                    'codigo_postal': predio1.codigo_postal,
                    'colonia': predio1.colonia.id,
                    'calle': predio1.calle.id,
                    'numero_exterior': predio1.numero_exterior,
                    'numero_interior': predio1.numero_interior,
                    'municipio_p': predio1.municipio.nombre,
                    'superficie_total': predio1.superficie_total,
                    'superficie_construida': predio1.superficie_construida,
                    'uso_predio': predio1.uso_predio,
                    'valor_catastral': predio1.valor_catastral,
                    'contribuyente': {
                        'id': contribuyente.id,
                        'tipoPersona': contribuyente.tipoPersona,
                        'homoclave': contribuyente.homoclave,
                        'rfc': contribuyente.rfc.upper() if contribuyente.rfc else '',
                        'curp': contribuyente.curp.upper() if contribuyente.curp else '',
                        'nombre': contribuyente.nombre.upper() if contribuyente.nombre else '',
                        'ApellidoP': contribuyente.apellidoP.upper() if contribuyente.apellidoP else '',
                        'ApellidoM': contribuyente.apellidoM.upper() if contribuyente.apellidoM else '',
                        'razonSocial': contribuyente.razonSocial.upper() if contribuyente.razonSocial else '',
                        'email': contribuyente.email.upper() if contribuyente.email else '',
                        'telefono': contribuyente.telefono,
                        'mc': contribuyente.mc,
                        'nombre_mc': contribuyente.nombre_mc.upper() if contribuyente.nombre_mc else '',
                        'ApellidoP_mc': contribuyente.apellidoP_mc.upper() if contribuyente.apellidoP_mc else '',
                        'ApellidoM_mc': contribuyente.apellidoM_mc.upper() if contribuyente.apellidoM_mc else '',
                    }
                }
                data.append(contrib_data)
            return JsonResponse({'predios': data})
        else:
            return JsonResponse({'error': 'No se encontró ningún predio con los datos proporcionados.'}, status=404)
    else:
        return JsonResponse({'error': 'Consulta vacía.'}, status=400)
def editar_noServicio(request, pk):
    servicio = get_object_or_404(noServicio, pk=pk)
    
    if request.method == 'POST':
        form = noServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El registro se ha editado correctamente!')
            return redirect('registrosAgua')  # Cambia 'registrosAgua' por el nombre de tu URL para la lista de servicios
    else:
        form = noServicioForm(instance=servicio)
    
    # Definir el contexto adicional aquí
    breadcrumb = {
        'parent': {'name': 'Registros de No. servicio', 'url': '/agua/registrosAgua/'},
        'child': {'name': 'Editar registro de numero de servicio', 'url': '/formularioAgua/'}
    }
    
    # Unir el contexto del formulario con el contexto adicional
    context = {
        'form': form,
        'edit_mode': True,
        'servicio': servicio,
        'breadcrumb': breadcrumb
    }
    
    return render(request, 'forms.html', context)


class cobroAgua(TemplateView):
    template_name = 'cobroAgua.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_month = datetime.now().strftime("%B")
        
        # Nombres de los meses en español
        months_es = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        # Obtener el nombre del mes actual en español
        month_index = datetime.now().month - 1
        current_month_es = months_es[month_index]
        
        context['months'] = months_es
        context['current_month'] = current_month_es

        context['breadcrumb'] = {
            'parent': {'name': 'Servicio de Agua Potable', 'url': '/agua/homeAgua/'},
            'child': {'name': 'Cobro de agua potable', 'url': '/cobroAgua/'}
        }
        return context



def obtener_predios(request):
    contribuyente_id = request.GET.get('contribuyente_id', None)
    if contribuyente_id:
        try:
            contribuyente = Contribuyente.objects.get(id=contribuyente_id)
            user = request.user
            
            # Obtener el municipio del usuario logueado
            municipio = user.Municipio
            predios = predio.objects.filter(contribuyente=contribuyente, municipio=municipio)
            
            predios_data = []
            for predio1 in predios:
                predios_data.append({
                    'id': predio1.id,
                    'descripcion': predio1.clave_catastral,  # Ajusta según los campos de tu modelo
                    'municipio': predio1.municipio.nombre,
                    'exte': f"{predio1.numero_exterior or ''}",
                    'inte': f"{predio1.numero_interior or ''}",
                    'calle':  predio1.calle.nombre,
                })
            
            return JsonResponse({'predios': predios_data})
        except Contribuyente.DoesNotExist:
            return JsonResponse({'error': 'Contribuyente no encontrado.'}, status=404)
    else:
        return JsonResponse({'error': 'ID de contribuyente vacío.'}, status=400)

def obtener_predio_detalle(request):
    predio_id = request.GET.get('predio_id', None)
    
    if predio_id:
        try:
            predio1 = get_object_or_404(predio, id=predio_id)
            predio_data = {
                'claveCatastral': predio1.clave_catastral,
                'predio': predio1.id,
                'estado': predio1.estado,
                'codigo_postal': predio1.codigo_postal,
                'municipio_predio': predio1.municipio.nombre,
                'colonia': predio1.colonia.id,
                'calle': predio1.calle.id,
                'numero_exterior': predio1.numero_exterior or '',
                'numero_interior': predio1.numero_interior or '',
                'superficie_total': predio1.superficie_total,
                'superficie_construida': predio1.superficie_construida,
                'uso_predio': predio1.uso_predio,
                'valor_catastral': predio1.valor_catastral,
                # Añade aquí el resto de campos del predio
            }
            return JsonResponse(predio_data)
        except predio.DoesNotExist:
            return JsonResponse({'error': 'Predio no encontrado.'}, status=404)
    else:
        return JsonResponse({'error': 'ID de predio vacío.'}, status=400)
    

