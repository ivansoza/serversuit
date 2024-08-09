from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models.functions import Lower, Upper
from django.http import JsonResponse
import json  # Necesario para parsear el cuerpo de la solicitud que está en formato JSON
from django.views.decorators.http import require_http_methods
from urllib.parse import unquote
from django.views.decorators.http import require_POST

from catalogos.models import Calle, Colonia, Estado, Municipio
from agua.models import noServicio
from contribuyente.models import Contribuyente
from predio.forms import PredioForm, PredioFormUpdate
from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from .models import predio
from django.http import JsonResponse
from django.db.models import Count, Q, Value, CharField,Subquery, OuterRef, IntegerField
from django.views.generic.edit import UpdateView
from django.db.models.functions import Coalesce

# Create your views here.


class homePredioView(TemplateView):
    template_name = 'homePredio.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Servicio de Predio'}
        }

        context['sidebar'] = 'predio'

        return context
    

class TablaRegistrosPredio(LoginRequiredMixin, ListView):
    model = predio
    template_name = 'registrosPredios.html'
    context_object_name = 'predios'

    def get_queryset(self):
        # Intenta obtener el municipio del usuario.
        try:
            municipio_usuario = self.request.user.Municipio
            return predio.objects.filter(municipio=municipio_usuario)
        except Municipio.DoesNotExist:
            # Si no existe el municipio para el usuario, redirecciona o muestra un mensaje.
            messages.error(self.request, 'Aún no se ha asociado un municipio con el usuario.')
            return predio.objects.none()  # Retorna un queryset vacío

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Servicio de Predio', 'url': '/predio/homePredio/'},
            'child': {'name': 'Registros de No. Predios'}
        }

        context['sidebar'] = 'predio'

        return context
    

class formularioPredio(LoginRequiredMixin, TemplateView):
    template_name = 'formsPredio.html'
    form_class = PredioForm
    success_url = reverse_lazy('registroPredios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Registros de No. Predios', 'url': '/predio/registrosPredio/'},
            'child': {'name': 'Formulario de Registro de Predios', 'url': '/formularioAgua/'}
        }
        # Establecer los valores iniciales aquí
        initial_data = {
            'registro': f"{self.request.user.first_name} {self.request.user.last_name}"
        }
        context['form'] = self.form_class(initial=initial_data)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            predio_instance = form.save(commit=False)
            predio_instance.codigo_postal = request.POST.get('codigo_postal')
            predio_instance.estado = request.POST.get('estado')

            if hasattr(request.user, 'Municipio') and request.user.Municipio:
                predio_instance.municipio = request.user.Municipio
            else:
                messages.error(request, 'No se puede hacer el registro debido a que el usuario que registra no tiene un municipio asignado.')
                return self.render_to_response(self.get_context_data(form=form))

            nombre_colonia = request.POST.get('colonia', '').strip()
            if nombre_colonia:
                colonia, created = Colonia.objects.get_or_create(
                    nombre__iexact=nombre_colonia,
                    municipio=request.user.Municipio,
                    defaults={'nombre': nombre_colonia}
                )
                predio_instance.colonia = colonia
            else:
                messages.error(request, 'El nombre de la colonia no puede estar vacío.')
                return self.render_to_response(self.get_context_data(form=form))

            calle_id = request.POST.get('calle', '').strip()
            if calle_id:
                calle = Calle.objects.filter(pk=calle_id, colonia=colonia).first()
                if calle:
                    predio_instance.calle = calle
                else:
                    # Si no se encuentra la calle con ese ID dentro de la colonia especificada, maneja el error
                    messages.error(request, 'La calle especificada no existe en la colonia seleccionada.')
                    return self.render_to_response(self.get_context_data(form=form))
            else:
                messages.error(request, 'Debe seleccionar una calle.')
                return self.render_to_response(self.get_context_data(form=form))

            predio_instance.save()
            messages.success(request, 'El registro se ha guardado correctamente.')
            return HttpResponseRedirect(self.success_url)
        else:
            # Utilizar form.errors para mostrar errores específicos de cada campo del formulario.
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')
            return self.render_to_response(self.get_context_data(form=form))


class FormularioPredioUpdate(LoginRequiredMixin, UpdateView):
    model = predio
    form_class = PredioFormUpdate
    template_name = 'editarPredio.html'
    success_url = reverse_lazy('registroPredios')

    def form_valid(self, form):
        predio_instance = form.save(commit=False)
        
        # Extracción de datos adicionales directamente del request.POST
        predio_instance.codigo_postal = self.request.POST.get('codigo_postal')
        predio_instance.estado = self.request.POST.get('estado')

        if hasattr(self.request.user, 'Municipio') and self.request.user.Municipio:
            predio_instance.municipio = self.request.user.Municipio
        else:
            messages.error(self.request, 'No se puede hacer el registro debido a que el usuario que registra no tiene un municipio asignado.')
            return self.form_invalid(form)

        nombre_colonia = self.request.POST.get('colonia', '').strip()
        if nombre_colonia:
            colonia, created = Colonia.objects.get_or_create(
                nombre__iexact=nombre_colonia,
                municipio=self.request.user.Municipio,
                defaults={'nombre': nombre_colonia}
            )
            predio_instance.colonia = colonia
        else:
            messages.error(self.request, 'El nombre de la colonia no puede estar vacío.')
            return self.form_invalid(form)

        calle_id = self.request.POST.get('calle', '').strip()
        if calle_id:
            calle = Calle.objects.filter(pk=calle_id, colonia=colonia).first()
            if calle:
                predio_instance.calle = calle
            else:
                messages.error(self.request, 'La calle especificada no existe en la colonia seleccionada.')
                return self.form_invalid(form)
        else:
            messages.error(self.request, 'Debe seleccionar una calle.')
            return self.form_invalid(form)

        predio_instance.save()
        messages.success(self.request, 'El registro se ha actualizado correctamente.')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        # Mostrar errores del formulario
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error en el campo {field}: {error}')
        return super().form_invalid(form)


def consultar_contribuyente(request):
    consulta = request.GET.get('consulta', None)
    if consulta:
        if len(consulta) == 9 or len(consulta) == 10:
            contribuyentes = Contribuyente.objects.filter(rfc__iexact=consulta)
        else:
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
            data = list(contribuyentes.values(
                'id', 'nombre', 'apellidoP', 'apellidoM', 'rfc', 'curp', 'homoclave', 
                'tipoPersona', 'razonSocial', 'mc', 'nombre_mc', 'apellidoP_mc', 'apellidoM_mc',
                'email', 'telefono'
            ))
            # Añadir domicilio utilizando el método get_full_address
            for contribuyente in data:
                obj = Contribuyente.objects.get(id=contribuyente['id'])
                contribuyente['domicilio'] = obj.get_full_address()  # Aquí se llama al método personalizado
                contribuyente['nombre'] = contribuyente['nombre'].upper() if contribuyente['nombre'] else ''
                contribuyente['apellidoP'] = contribuyente['apellidoP'].upper() if contribuyente['apellidoP'] else ''
                contribuyente['apellidoM'] = contribuyente['apellidoM'].upper() if contribuyente['apellidoM'] else ''
                contribuyente['rfc'] = contribuyente['rfc'].upper() if contribuyente['rfc'] else ''
                contribuyente['curp'] = contribuyente['curp'].upper() if contribuyente['curp'] else ''
                contribuyente['homoclave'] = contribuyente['homoclave'].upper() if contribuyente['homoclave'] else ''
                contribuyente['razonSocial'] = contribuyente['razonSocial'].upper() if contribuyente['razonSocial'] else ''
                contribuyente['nombre_mc'] = contribuyente['nombre_mc'].upper() if contribuyente['nombre_mc'] else ''
                contribuyente['apellidoP_mc'] = contribuyente['apellidoP_mc'].upper() if contribuyente['apellidoP_mc'] else ''
                contribuyente['apellidoM_mc'] = contribuyente['apellidoM_mc'].upper() if contribuyente['apellidoM_mc'] else ''
                contribuyente['email'] = contribuyente['email'] if contribuyente['email'] else ''

            return JsonResponse(data, safe=False, status=200)
        else:
            return JsonResponse({'mensaje': 'Contribuyente no encontrado'}, status=404)
    return JsonResponse({'error': 'Consulta vacía'}, status=400)


def consultar_contribuyente_op(request):
    consulta = request.GET.get('consulta', None)
    if consulta:
        if len(consulta) == 9 or len(consulta) == 10:
            contribuyentes = Contribuyente.objects.filter(rfc__iexact=consulta)
        else:
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
   
            predios_subquery = Subquery(
                predio.objects.filter(
                    contribuyente=OuterRef('pk'),
                    municipio=request.user.Municipio  # Asegúrate de que 'Municipio' es el campo correcto
                ).order_by().values('contribuyente').annotate(total=Count('id')).values('total'),
                output_field=IntegerField()
            )

            # Subquery para contar servicios de agua, asociados al contribuyente
            servicios_subquery = Subquery(
                noServicio.objects.filter(
                    contri=OuterRef('pk')  # Usando el related_name 'noservicios'
                ).order_by().values('contri').annotate(total=Count('id')).values('total'),
                output_field=IntegerField()
            )
            contribuyentes = contribuyentes.annotate(
                predios_count=Coalesce(predios_subquery, 0),
                noservicios_count=Coalesce(servicios_subquery, 0)
            )

            data = list(contribuyentes.values(
                'id', 'nombre', 'apellidoP', 'apellidoM', 'rfc', 'curp', 'homoclave',
                'tipoPersona', 'razonSocial', 'mc', 'nombre_mc', 'apellidoP_mc', 'apellidoM_mc',
                'email', 'telefono', 'predios_count', 'noservicios_count'
            ))

            # Añadir más datos como el domicilio
            for contribuyente in data:
                obj = Contribuyente.objects.get(id=contribuyente['id'])
                contribuyente['domicilio'] = obj.get_full_address() if hasattr(obj, 'get_full_address') else 'Dirección no disponible'
                contribuyente['nombre'] = contribuyente['nombre'].upper() if contribuyente['nombre'] else ''
                contribuyente['apellidoP'] = contribuyente['apellidoP'].upper() if contribuyente['apellidoP'] else ''
                contribuyente['apellidoM'] = contribuyente['apellidoM'].upper() if contribuyente['apellidoM'] else ''
                contribuyente['rfc'] = contribuyente['rfc'].upper() if contribuyente['rfc'] else ''
                contribuyente['curp'] = contribuyente['curp'].upper() if contribuyente['curp'] else ''
                contribuyente['homoclave'] = contribuyente['homoclave'].upper() if contribuyente['homoclave'] else ''
                contribuyente['razonSocial'] = contribuyente['razonSocial'].upper() if contribuyente['razonSocial'] else ''
                contribuyente['nombre_mc'] = contribuyente['nombre_mc'].upper() if contribuyente['nombre_mc'] else ''
                contribuyente['apellidoP_mc'] = contribuyente['apellidoP_mc'].upper() if contribuyente['apellidoP_mc'] else ''
                contribuyente['apellidoM_mc'] = contribuyente['apellidoM_mc'].upper() if contribuyente['apellidoM_mc'] else ''
                contribuyente['email'] = contribuyente['email'] if contribuyente['email'] else ''

            return JsonResponse(data, safe=False, status=200)
        else:
            return JsonResponse({'mensaje': 'Contribuyente no encontrado'}, status=404)
    return JsonResponse({'error': 'Consulta vacía'}, status=400)

def buscar_municipio(request):
    nombre = request.GET.get('nombre', '').strip()
    if not nombre:
        return JsonResponse({'error': 'No se proporcionó un nombre válido'}, status=400)

    # Intenta encontrar el municipio en minúsculas
    municipio = Municipio.objects.annotate(
        nombre_lower=Lower('nombre')
    ).filter(nombre_lower=nombre.lower()).first()

    if not municipio:
        # Si no se encuentra, intenta en mayúsculas
        municipio = Municipio.objects.annotate(
            nombre_upper=Upper('nombre')
        ).filter(nombre_upper=nombre.upper()).first()

    if not municipio:
        # Si aún no se encuentra, intenta con la primera letra de cada palabra en mayúscula
        nombre_capitalizado = ' '.join(word.capitalize() for word in nombre.split())
        municipio = Municipio.objects.filter(nombre__exact=nombre_capitalizado).first()

    if municipio:
        return JsonResponse({'id': municipio.id})
    else:
        return JsonResponse({'error': 'Municipio no encontrado'}, status=404)
    
@login_required
@require_POST
def add_calle(request):
    data = json.loads(request.body)
    
    def clean_name(name):
        # Quitar espacios adicionales y capitalizar
        cleaned_name = name.strip().capitalize()
        # Eliminar todos los puntos finales
        while cleaned_name.endswith('.'):
            cleaned_name = cleaned_name[:-1].strip()
        return cleaned_name
    
    nombre_calle = clean_name(data.get('nombre', ''))
    nombre_colonia = clean_name(data.get('colonia', ''))

    # Obtener el municipio del usuario autenticado
    municipio_usuario = request.user.Municipio
    if not municipio_usuario:
        return JsonResponse({'success': False, 'error': 'No se ha asignado un municipio al usuario.'}, status=400)

    # Buscar o crear la colonia asociada al municipio del usuario
    colonia, created = Colonia.objects.get_or_create(
        nombre__iexact=nombre_colonia,
        municipio=municipio_usuario,
        defaults={'nombre': nombre_colonia}  # Asegúrate de que el nombre está capitalizado correctamente al crear
    )

    # Verificar si ya existe una calle con el mismo nombre en la colonia
    if Calle.objects.filter(nombre__iexact=nombre_calle, colonia=colonia).exists():
        return JsonResponse({'success': False, 'error': 'Ya existe una calle con ese nombre en la colonia seleccionada.'}, status=400)

    # Crear la nueva calle si no existe
    new_calle = Calle.objects.create(nombre=nombre_calle, colonia=colonia)
    
    return JsonResponse({'success': True, 'id': new_calle.id, 'nombre': new_calle.nombre.upper()})


@login_required
@require_POST
def add_calle_general(request):
    data = json.loads(request.body)
    
    def clean_name(name):
        cleaned_name = name.strip().capitalize()
        while cleaned_name.endswith('.'):
            cleaned_name = cleaned_name[:-1].strip()
        return cleaned_name

    nombre_calle = clean_name(data.get('nombre', ''))
    nombre_colonia = clean_name(data.get('colonia', ''))
    nombre_estado = clean_name(data.get('estado', ''))
    nombre_municipio = clean_name(data.get('municipio', ''))

    # Procesar el estado
    estado, estado_created = Estado.objects.get_or_create(
        nombre__iexact=nombre_estado,
        defaults={'nombre': nombre_estado}
    )
    if estado_created:
        estado.numero_estado = 1  # Asegúrate de asignar un valor por defecto aquí
        estado.save()

    # Procesar el municipio
    municipio, municipio_created = Municipio.objects.get_or_create(
        nombre__iexact=nombre_municipio,
        estado=estado, 
        defaults={'nombre': nombre_municipio}
    )
    if municipio_created:
        municipio.numero_municipio = 1  # Asigna un número inicial, ajusta según necesites
        municipio.save()

    colonia, colonia_created = Colonia.objects.get_or_create(
        nombre__iexact=nombre_colonia,
        municipio=municipio,
        defaults={'nombre': nombre_colonia}
    )

    if Calle.objects.filter(nombre__iexact=nombre_calle, colonia=colonia).exists():
        return JsonResponse({'success': False, 'error': 'Ya existe una calle con ese nombre en la colonia seleccionada.'}, status=400)

    new_calle = Calle.objects.create(nombre=nombre_calle, colonia=colonia)
    
    return JsonResponse({'success': True, 'id': new_calle.id, 'nombre': new_calle.nombre.upper()})

@login_required
def get_calles_by_colonia(request, colonia_nombre):
    colonia_nombre_decoded = unquote(colonia_nombre)

    user_municipio_id = request.user.Municipio.id if hasattr(request.user, 'Municipio') and request.user.Municipio else None
    if not user_municipio_id:
        return JsonResponse({'error': 'Usuario no tiene un municipio asociado'}, status=400)

    calles = Calle.objects.filter(
        colonia__nombre__iexact=colonia_nombre_decoded,
        colonia__municipio_id=user_municipio_id
    ).order_by('nombre')
    calles_uppercase = [{'id': calle.id, 'nombre': calle.nombre.upper()} for calle in calles]  # Cambio aquí

    return JsonResponse({'calles': calles_uppercase})



@login_required
def get_calles_by_colonia_general(request, estado_nombre, municipio_nombre, colonia_nombre):
    estado_nombre_decoded = unquote(estado_nombre).capitalize()
    municipio_nombre_decoded = unquote(municipio_nombre).capitalize()
    colonia_nombre_decoded = unquote(colonia_nombre).capitalize()

    # Buscar el estado
    estado = Estado.objects.filter(nombre__iexact=estado_nombre_decoded).first()
    if not estado:
        return JsonResponse({'error': 'Estado no encontrado', 'calles': []}, status=200)

    # Buscar el municipio dentro del estado
    municipio = Municipio.objects.filter(nombre__iexact=municipio_nombre_decoded, estado=estado).first()
    if not municipio:
        return JsonResponse({'error': 'Municipio no encontrado en el estado proporcionado', 'calles': []}, status=200)

    # Buscar la colonia dentro del municipio
    colonia = Colonia.objects.filter(nombre__iexact=colonia_nombre_decoded, municipio=municipio).first()
    if not colonia:
        return JsonResponse({'error': 'Colonia no encontrada en el municipio proporcionado', 'calles': []}, status=200)

    # Obtener calles de la colonia
    calles = Calle.objects.filter(colonia=colonia).order_by('nombre')
    calles_uppercase = [{'id': calle.id, 'nombre': calle.nombre.upper()} for calle in calles]

    return JsonResponse({'calles': calles_uppercase if calles else []})

@login_required
def verify_user_location(request):
    estado_nombre = request.GET.get('estado', '').strip()
    municipio_nombre = request.GET.get('municipio', '').strip()

    user_municipio = request.user.Municipio
    if not user_municipio:
        return JsonResponse({'success': False, 'message': 'No tiene municipio registrado.'})
    
    # Verificar estado insensible a mayúsculas/minúsculas
    if not Estado.objects.filter(nombre__iexact=estado_nombre, id=user_municipio.estado.id).exists():
        return JsonResponse({'success': False, 'message': 'El estado no coincide con el registrado para el usuario.'})
    
    # Verificar municipio insensible a mayúsculas/minúsculas
    if not Municipio.objects.filter(nombre__iexact=municipio_nombre, id=user_municipio.id).exists():
        return JsonResponse({'success': False, 'message': 'El municipio no coincide con el registrado para el usuario.'})

    return JsonResponse({'success': True})