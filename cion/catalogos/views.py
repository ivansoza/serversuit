from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth import update_session_auth_hash

from catalogos.models import Municipio, PersonalizacionTema, Descuentos,Recargos, areasMunicipio, areas, ServicioMunicipio, Servicios
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
import logging
import os
from django.views.generic import CreateView

from cionapp.models import PaginaInicio
from usuarios.models import CustomUser
from .forms import CustomPasswordChangeForm, CustomUserCreationForm, PaginaInicioForm, ServicioMunicipioForms, descuentoRecargoForm, AreasMunicipioForm, AreasForms, ServiciosForms, recargoForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q
from django.views import generic

from django.urls import reverse

class ConfiguracionView(TemplateView):
    template_name = 'configuracion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Configuración'}
        }
        return context
    
    
class PasswordChangeView(LoginRequiredMixin, generic.FormView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('configuracion')  # Asegúrate de que esta URL esté definida en tu urls.py
    template_name = 'cambiar_contraseña.html' 

    def form_valid(self, form):
        form.save()
        # Actualizar la sesión del usuario para que no se cierre al cambiar la contraseña
        update_session_auth_hash(self.request, form.user)
        # Añadir mensaje de éxito
        messages.success(self.request, 'Tu contraseña ha sido actualizada exitosamente.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('configuracion')
        context['breadcrumb'] = {
            'parent': {'name': 'Configuración', 'url': url_configuracion},
            'child': {'name': 'Cambiar Contraseña'}
        }
        return context
class PersonalizacionView(TemplateView):
    template_name = 'personalizacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_configuracion = reverse('configuracion')
        context['breadcrumb'] = {
            'parent': {'name': 'Configuración', 'url': url_configuracion},
            'child': {'name': 'Personalización de la Interfaz'}
        }
        context['sidebar'] = 'personalizacion'
        
        user = self.request.user
        if user.is_authenticated:
            try:
                municipio = user.Municipio
                personalizacion = PersonalizacionTema.objects.get(municipio=municipio)
                context['logotipo_url'] = personalizacion.logotipo.url if personalizacion.logotipo else None
                context['logotipo_nombre'] = os.path.basename(personalizacion.logotipo.name)  # Solo el nombre del archivo
                context['logotipo_size'] = personalizacion.logotipo.size if personalizacion.logotipo else None
            except (Municipio.DoesNotExist, PersonalizacionTema.DoesNotExist):
                context['logotipo_url'] = None
                context['logotipo_nombre'] = None
                context['logotipo_size'] = None
        
        return context
class PersonalizacionInfoView(TemplateView):
    template_name = 'personalizacionHome.html'

    def get_context_data(self, **kwargs):
        url_configuracion = reverse('configuracion')

        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Configuración', 'url': url_configuracion},
            'child': {'name': 'Información del Municipio'}
        }
        context['sidebar'] = 'personalizacion'
        user = self.request.user
        if user.is_authenticated:
            municipio = getattr(user, 'Municipio', None)
            if municipio:
                instance, created = PaginaInicio.objects.get_or_create(municipio=municipio)
                context['fondo_url'] = instance.imagen_inicio.url if instance.imagen_inicio else None
                context['organigrama_url'] = instance.imagen_organigrama.url if instance.imagen_organigrama else None
                form = PaginaInicioForm(instance=instance)
            else:
                form = PaginaInicioForm()
                context['fondo_url'] = None
                context['organigrama_url'] = None

                messages.error(self.request, "Este usuario no tiene un municipio asignado.")
        else:
            form = PaginaInicioForm()
            context['fondo_url'] = None
            context['organigrama_url'] = None
            messages.error(self.request, "Debe iniciar sesión para acceder a esta función.")

        context['form'] = form
        return context
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            municipio = getattr(user, 'Municipio', None)
            if municipio:
                instance, created = PaginaInicio.objects.get_or_create(municipio=municipio)
                form = PaginaInicioForm(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Información actualizada con éxito.")
                    return redirect('PersonalizacionInfoView')
                else:
                    messages.error(request, "Por favor corrija los errores en el formulario.")
            else:
                messages.error(request, "Este usuario no tiene un municipio asignado.")
        else:
            messages.error(request, "Debe iniciar sesión para acceder a esta función.")
        return self.render_to_response(self.get_context_data(form=form))



@require_http_methods(["POST"])
def actualizar_personalizacion1(request):

    # Ensure the user has an associated municipio before proceeding
    if not hasattr(request.user, 'Municipio') or request.user.Municipio is None:
        messages.error(request, 'Este usuario no tiene un municipio asignado.')
        return redirect('personalizacion')
    
    municipio = request.user.Municipio

    tipo_diseno = request.POST.get('tipo_diseno', '').upper()
    tipo_sidebar = request.POST.get('tipo_sidebar', '').upper()
    tipo_icono_sidebar = request.POST.get('tipo_icono_sidebar', '').upper()
    color_1 = request.POST.get('color_1', 'Default')
    color_1a = request.POST.get('color_1a', 'Default')
    color_2 = request.POST.get('color_2', 'Default')
    color_2a = request.POST.get('color_2a', 'Default')


    try:
        personalizacion, created = PersonalizacionTema.objects.update_or_create(
            municipio=municipio,
            defaults={
                'tipo_diseno': tipo_diseno,
                'tipo_sidebar': tipo_sidebar,
                'tipo_icono_sidebar': tipo_icono_sidebar,
                'color_1': color_1,
                'color_1a': color_1a,
                'color_2': color_2,
                'color_2a': color_2a
            }
        )
        if created:
            pass
        else:
            pass
        messages.success(request, 'La personalización ha sido actualizada con éxito.')
    except Exception as e:
        messages.error(request, f"An error occurred while updating: {str(e)}")

    return redirect('personalizacion')



@require_http_methods(["POST"])
def subir_logotipo(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debe iniciar sesión para acceder a esta función.")
        return redirect('login')
    try:
        municipio = request.user.Municipio  
        
    except Municipio.DoesNotExist:
        messages.error(request, "Este usuario no tiene un municipio asignado.")
        return redirect('personalizacion')

    file = request.FILES.get('file')

    if not file:
        messages.error(request, "No se encontró ningún archivo para subir.")
        return redirect('personalizacion')

    valid_image_mimetypes = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in valid_image_mimetypes:
        messages.error(request, "Archivo no compatible. Solo se permiten imágenes JPEG, PNG, GIF o WebP.")
        return redirect('personalizacion')
    try:
        # Obtener la instancia actual de PersonalizacionTema para el municipio
        personalizacion = PersonalizacionTema.objects.filter(municipio=municipio).first()

        # Si ya existe una personalización y tiene un logotipo, eliminar el archivo anterior
        if personalizacion and personalizacion.logotipo:
            if os.path.isfile(personalizacion.logotipo.path):
                os.remove(personalizacion.logotipo.path)

        # Crear o actualizar la personalización con el nuevo logotipo
        personalizacion, created = PersonalizacionTema.objects.update_or_create(
            municipio=municipio,
            defaults={'logotipo': file}
        )
        messages.success(request, "La personalización ha sido actualizada con éxito.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al actualizar la personalización: {str(e)}")
        return redirect('personalizacion')

    return redirect('personalizacion')

@require_http_methods(["POST"])
def subir_imagen_inicio(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debe iniciar sesión para acceder a esta función.")
        return redirect('login')

    try:
        municipio = request.user.Municipio
    except Municipio.DoesNotExist:
        messages.error(request, "Este usuario no tiene un municipio asignado.")
        return redirect('PersonalizacionInfoView')

    file = request.FILES.get('file')
    if not file:
        messages.error(request, "No se encontró ningún archivo para subir.")
        return redirect('PersonalizacionInfoView')

    valid_image_mimetypes = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in valid_image_mimetypes:
        messages.error(request, "Archivo no compatible. Solo se permiten imágenes JPEG, PNG, GIF o WebP.")
        return redirect('PersonalizacionInfoView')

    try:
        pagina_inicio = PaginaInicio.objects.filter(municipio=municipio).first()

        # Si ya existe una página de inicio y tiene una imagen, eliminar el archivo anterior
        if pagina_inicio and pagina_inicio.imagen_inicio:
            if os.path.isfile(pagina_inicio.imagen_inicio.path):
                os.remove(pagina_inicio.imagen_inicio.path)

        # Crear o actualizar la página de inicio con la nueva imagen
        pagina_inicio, created = PaginaInicio.objects.update_or_create(
            municipio=municipio,
            defaults={'imagen_inicio': file}
        )
        messages.success(request, "La imagen de inicio ha sido actualizada con éxito.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al actualizar la imagen de inicio: {str(e)}")
        return redirect('PersonalizacionInfoView')

    return redirect('PersonalizacionInfoView')

@require_http_methods(["POST"])
def subir_imagen_organigrama(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debe iniciar sesión para acceder a esta función.")
        return redirect('login')

    try:
        municipio = request.user.Municipio
    except Municipio.DoesNotExist:
        messages.error(request, "Este usuario no tiene un municipio asignado.")
        return redirect('PersonalizacionInfoView')

    file = request.FILES.get('file')
    if not file:
        messages.error(request, "No se encontró ningún archivo para subir.")
        return redirect('PersonalizacionInfoView')

    valid_image_mimetypes = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in valid_image_mimetypes:
        messages.error(request, "Archivo no compatible. Solo se permiten imágenes JPEG, PNG, GIF o WebP.")
        return redirect('PersonalizacionInfoView')

    try:
        pagina_inicio = PaginaInicio.objects.filter(municipio=municipio).first()

        # Si ya existe una página de inicio y tiene una imagen de organigrama, eliminar el archivo anterior
        if pagina_inicio and pagina_inicio.imagen_organigrama:
            if os.path.isfile(pagina_inicio.imagen_organigrama.path):
                os.remove(pagina_inicio.imagen_organigrama.path)

        # Crear o actualizar la página de inicio con la nueva imagen de organigrama
        pagina_inicio, created = PaginaInicio.objects.update_or_create(
            municipio=municipio,
            defaults={'imagen_organigrama': file}
        )
        messages.success(request, "La imagen del organigrama ha sido actualizada con éxito.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al actualizar la imagen del organigrama: {str(e)}")
        return redirect('PersonalizacionInfoView')

    return redirect('PersonalizacionInfoView')


class homeCatalogos(TemplateView):
    template_name='homeCatalogos.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Catalogos', 'url': '/homeCatalogos/'}
        }
        return context
def obtener_municipio_usuario(request):
    if request.user.is_authenticated:
        usuario = request.user
        municipio_usuario = usuario.Municipio  # Ajusta esto según tu modelo de Usuario
        return municipio_usuario
    return None 



class tablaDescuentos(TemplateView):
    template_name = 'descuentos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Catálogos', 'url': '/personalizacion/homeCatalogos'},
            'child': {'name': 'Descuentos y recargos', 'url': '/tablaDescuentos/'}
        }
        municipio_usuario = self.request.user.Municipio
        context['descuento_form'] = descuentoRecargoForm(initial={'municipio': municipio_usuario})
        context['recargo_form'] = recargoForm(initial={'municipio': municipio_usuario})

        # Obtener los registros filtrados por municipio del usuario logueado
        descuentos = Descuentos.objects.filter(municipio=municipio_usuario)
        recargos = Recargos.objects.filter(municipio=municipio_usuario)
        # Contar los registros de tipo Descuento y Recargo
        context['descuento_count'] = descuentos.count()
        context['recargo_count'] = recargos.count()
        # Combinar los registros de descuentos y recargos
        context['registros'] = list(descuentos) + list(recargos)

        return context

    def post(self, request, *args, **kwargs):
        form_id = request.POST.get('form_id')
        
        if 'guardar_descuento' in request.POST:
            if form_id:
                # Editar descuento existente
                descuento = get_object_or_404(Descuentos, id=form_id)
                descuento_form = descuentoRecargoForm(request.POST, instance=descuento)
            else:
                # Crear nuevo descuento
                descuento_form = descuentoRecargoForm(request.POST)
            
            if descuento_form.is_valid():
                descuento_form.save()
                messages.success(request, 'El descuento se ha guardado correctamente.')
                return redirect('tablaDescuentos')

        elif 'guardar_recargo' in request.POST:
            if form_id:
                # Editar recargo existente
                recargo = get_object_or_404(Recargos, id=form_id)
                recargo_form = recargoForm(request.POST, instance=recargo)
            else:
                # Crear nuevo recargo
                recargo_form = recargoForm(request.POST)
            
            if recargo_form.is_valid():
                recargo_form.save()
                messages.success(request, 'El recargo se ha guardado correctamente.')
                return redirect('tablaDescuentos')

        # Si el formulario no es válido, o el método POST no coincide, vuelve a cargar los formularios en el contexto
        context = self.get_context_data()
        if 'guardar_descuento' in request.POST:
            context['descuento_form'] = descuento_form
        elif 'guardar_recargo' in request.POST:
            context['recargo_form'] = recargo_form
        return self.render_to_response(context)

    
    
def editar_descuento(request, id):
    descuento = get_object_or_404(Descuentos, id=id)

    if request.method == 'POST':
        form = descuentoRecargoForm(request.POST, instance=descuento)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El registro se ha editado correctamente!')
            return redirect('tablaDescuentos')  # Cambia 'registrosAgua' por el nombre de tu URL para la lista de servicios
        else:
            # Si el formulario no es válido, puedes retornar errores
            return JsonResponse({'error': form.errors}, status=400)

    # Si es GET, renderiza el formulario para editar el descuento
    form = descuentoRecargoForm(instance=descuento)
    return render(request, 'descuentos.html', {'form': form, 'descuento': descuento, 'edit_mode': True})

def obtener_registro(request, id):
    descuento = get_object_or_404(Descuentos, id=id)
    data = {
        'id': descuento.id,
        'tipo': descuento.tipo,
        'nombre': descuento.nombre,
        'porcentaje': descuento.porcentaje,
        'monto': descuento.monto,
    }
    return JsonResponse(data)

@csrf_exempt
def eliminar_descuento(request, id):
    if request.method == 'DELETE':
        try:
            descuento = get_object_or_404(Descuentos, id=id)
            municipio_usuario = obtener_municipio_usuario(request)
            
            if municipio_usuario:
                descuento.delete()
                descuentos_count = Descuentos.objects.filter(municipio=municipio_usuario, tipo='Descuento').count()
                recargos_count = Descuentos.objects.filter(municipio=municipio_usuario, tipo='Recargo').count()
                
                return JsonResponse({'success': True, 'descuentos_count': descuentos_count, 'recargos_count': recargos_count})
            else:
                return JsonResponse({'success': False, 'error': 'Usuario sin municipio asignado'}, status=400)
        
        except Descuentos.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Registro no encontrado'}, status=404)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


class tablaArea(TemplateView):
    template_name = 'areas.html'
    form_class = AreasMunicipioForm
    areas_form_class = AreasForms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        municipio_usuario = self.request.user.Municipio
        context['breadcrumb'] = {
            'parent': {'name': 'Catalogos', 'url': '/personalizacion/homeCatalogos/'},
            'child': {'name': 'Areas', 'url': '/tablaArea/'}
        }

        try:
            area_municipio = areasMunicipio.objects.get(municipio=municipio_usuario)
            context['form'] = self.form_class(instance=area_municipio, municipio_usuario=municipio_usuario)
            context['edit'] = True
            context['muni']= area_municipio
            context['areas_municipio'] = area_municipio.area.all()
            context['count_areas'] = area_municipio.area.all().count
        except areasMunicipio.DoesNotExist:
            initial_data = {'municipio': municipio_usuario}
            context['form'] = self.form_class(initial=initial_data, municipio_usuario=municipio_usuario)
            context['edit'] = False
            context['areas_municipio'] = []
        initial_data = {'municipios_visibles': self.request.user.Municipio}
        context['areas'] = areas.obtener_areas_visibles(self.request.user)
        context['areas_form'] = self.areas_form_class(initial=initial_data)  # Agregar el formulario de áreas
        return context

    def post(self, request, *args, **kwargs):
        municipio_usuario = self.request.user.Municipio
        try:
            area_municipio = areasMunicipio.objects.get(municipio=municipio_usuario)
            form = self.form_class(request.POST, instance=area_municipio, municipio_usuario=municipio_usuario)
        except areasMunicipio.DoesNotExist:
            form = self.form_class(request.POST, municipio_usuario=municipio_usuario)

        if form.is_valid():
            form.save()
            messages.success(request, 'La selección de áreas se ha guardado correctamente.')
            return redirect('tablaArea')  # Redirige a la vista que desees después de guardar el formulario
        form2 = self.areas_form_class(request.POST)
        if form2.is_valid():
            form2.save()
            messages.success(request, 'Nueva áreas registrada.')
            return redirect('tablaArea')  # Redirige a la vista que desees después de guardar el formulario

        context = self.get_context_data()
        context['form'] = form
        context['areas_form'] = form2  # Agregar el formulario de áreas con datos POST
        return self.render_to_response(context)

#----------------------------------- MODELO SERVICIO------------------------------------------------------

class tablaServicios(TemplateView):
    template_name = 'servicios.html'
    form_class = ServicioMunicipioForms
    server_form_class = ServiciosForms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        municipio_usuario = self.request.user.Municipio

        # Obtener los registros de ServicioMunicipio que son visibles para el usuario logueado
        registros_servicios = ServicioMunicipio.objects.filter(
            Q(municipio=None) | Q(municipio=municipio_usuario)
        )

        context['breadcrumb'] = {
            'parent': {'name': 'Catalogos', 'url': '/personalizacion/homeCatalogos/'},
            'child': {'name': 'Servicios', 'url': '/tablaServicios/'}
        }
        context['registros_servicios'] = registros_servicios
        context['registros_servicios_count'] = registros_servicios.count()
        context['form'] = self.form_class(initial={'municipio': municipio_usuario}, municipio_usuario=municipio_usuario)
        initial_data = {'municipios_visibles': self.request.user.Municipio}
        context['ser_form'] = self.server_form_class(initial=initial_data)  # Agregar el formulario de áreas
        return context

    def post(self, request, *args, **kwargs):
        municipio_usuario = request.user.Municipio
        form = self.form_class(request.POST, municipio_usuario=municipio_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio de municipio guardado correctamente.')
            return redirect('tablaServicios')
        
        form2 = self.server_form_class(request.POST)
        if form2.is_valid():
            form2.save()
            messages.success(request, 'Nuevo Servicio registrado.')
            return redirect('tablaServicios')  # Redirige a la vista que desees después de guardar el formulario

        context = self.get_context_data()
        context['form'] = form
        context['ser_form'] = form2  # Agregar el formulario de áreas con datos POST
        return self.render_to_response(context)


def obtener_registro_servicio(request, id):
    servicio = get_object_or_404(ServicioMunicipio, pk=id)
    data = {
        'clave_id': servicio.clave.id,
        'municipio_id': servicio.municipio.id,
        'concepto': servicio.concepto,
        'monto': servicio.monto,
        'area': servicio.area.id,
    }
    return JsonResponse(data)

def editar_servicio(request, id):
    servicio = get_object_or_404(ServicioMunicipio, id=id)

    if request.method == 'POST':
        form = ServicioMunicipioForms(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El registro se ha editado correctamente!')
            return redirect('tablaServicios')  # Cambia 'registrosAgua' por el nombre de tu URL para la lista de servicios
        else:
            # Si el formulario no es válido, puedes retornar errores
            return JsonResponse({'error': form.errors}, status=400)

    # Si es GET, renderiza el formulario para editar el descuento
    form = ServicioMunicipioForms(instance=servicio)
    return render(request, 'servicios.html', {'form': form, 'descuento': servicio, 'edit_mode': True})
class homeCatalogos(TemplateView):
    template_name='homeCatalogos.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Catalogos', 'url': '/homeCatalogos/'}
        }

        context['sidebar'] = 'catalogo'

        return context
    

class CustomUserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registerUser.html'
    success_url = reverse_lazy('customuser_list')  # Asegúrate de cambiar 'detalle_familiares' por tu URL de destino.


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['municipio'] = self.request.user.Municipio
        return kwargs
    

    def form_valid(self, form):
        if not self.request.user.Municipio:
            return self.handle_no_municipio(form)

        # Guardar el nuevo usuario creado por el administrador sin guardar en la base de datos
        new_user = form.save(commit=False)
        # Asignar el municipio del request.user al nuevo usuario
        new_user.Municipio = self.request.user.Municipio
        new_user.save()
        # Mostrar un mensaje de éxito
        messages.success(self.request, "Usuario agregado con éxito.")
        return super().form_valid(form)
    def form_invalid(self, form):
        # Mostrar un mensaje de error cuando el formulario no es válido
        messages.error(self.request, "Error al agregar el usuario. Por favor, corrija los errores del formulario.")
        return super().form_invalid(form)

    def handle_no_municipio(self, form):
        # Mostrar un mensaje de error específico cuando el municipio no está asignado
        messages.error(self.request, "El usuario que está registrando no cuenta aún con municipio asignado. Por favor, asígnale un municipio.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Lista de Usuarios', 'url': '/personalizacion/usuarios'},
            'child': {'name': 'Registrar Usuario'}
        }

        context['sidebar'] = 'catalogo'

        return context
    
class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'customuser_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Lista de Usuarios'}
        }
        context['sidebar'] = 'catalogo'
        return context

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        is_active = request.POST.get('user_status') == 'True'
        user = CustomUser.objects.get(id=user_id)
        # Asegurarse de que el usuario no esté intentando desactivarse a sí mismo
        if user == request.user:
            messages.error(request, 'No puede cambiar su propio estado.')
            return redirect(reverse_lazy('customuser_list'))
        user.is_active = is_active
        user.save()
        messages.success(request, f'El estado de "{user.username}" ha sido actualizado a {"activo" if is_active else "inactivo"}.')
        return redirect(reverse_lazy('customuser_list'))
    def get_queryset(self):
        queryset = super().get_queryset()
        municipio_usuario_actual = self.request.user.Municipio
        
        # Filtrar solo usuarios que tienen el mismo municipio que el usuario actual
        if municipio_usuario_actual:
            queryset = queryset.filter(Municipio=municipio_usuario_actual)
        else:
            # Si el usuario actual no tiene municipio asignado, no mostrar usuarios
            queryset = CustomUser.objects.none()
        
        # Excluir al usuario actual del queryset
        queryset = queryset.exclude(id=self.request.user.id)

        for user in queryset:
            user.full_name = f"{user.first_name} {user.last_name} {' ' + user.apellido_materno if user.apellido_materno else ''}".strip()
            user.email = user.email if user.email else 'N/A'
            user.apellido_materno = user.apellido_materno if user.apellido_materno else ''

        return queryset
    
