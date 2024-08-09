from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, ListView

from catalogos.models import Calle
from .models import Contribuyente
from .forms import InformacionContribuyenteForm, DomicilioForm, InformacionFiscalForm, InformacionFiscalFormUpdate
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse

class HomeContribuyente(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            'parent': {'name': 'Dashboard'},
            'child': {'name': 'Contribuyente', 'url': '/home_ctr/'}
        }
        context['sidebar'] = 'home_contribuyente'
        return context
    
class ListContribuyentes(ListView):
    model = Contribuyente
    template_name = 'listaCtr.html'
    context_object_name = 'registros'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = {
            # 'parent': {'name': 'Contribuyente'},
            'parent': {'name': 'Contribuyente', 'url': '/contribuyente/home/'},
            'child': {'name': 'Registros de Contribuyentes', 'url': '/home_ctr/'}
        }
        context['sidebar'] = 'home_contribuyente'
        return context

class RegistroContribuyenteView(View):

    
    def post(self, request, *args, **kwargs):
        form1 = InformacionContribuyenteForm(request.POST, request.FILES, prefix='informacion_contribuyente')
        form2 = DomicilioForm(request.POST, request.FILES, prefix='domicilio')
        form3 = InformacionFiscalForm(request.POST, request.FILES, prefix='informacion_fiscal')

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            contribuyente = Contribuyente()

            # Asignar los datos limpios de cada formulario a la instancia del modelo
            for field, value in form1.cleaned_data.items():
                setattr(contribuyente, field, value)
            for field, value in form2.cleaned_data.items():
                setattr(contribuyente, field, value)
            for field, value in form3.cleaned_data.items():
                setattr(contribuyente, field, value)

            # Obtener y asignar datos adicionales de domicilio
            calle_id = request.POST.get('calle', '').strip()  # Usando 'calle' como clave en POST
            if calle_id:
                calle = Calle.objects.filter(id=calle_id).first()
                if calle:
                    contribuyente.calle = calle
                    contribuyente.colonia = calle.colonia
                    contribuyente.municipio = calle.colonia.municipio

            contribuyente.cp = request.POST.get('codigo_postal')
            
            # Guardar la instancia del modelo en la base de datos
            contribuyente.save()
            messages.success(request, 'Contribuyente creado con éxito')  # Agregar el mensaje de éxito

            return redirect('lista_ctr')  # Redirigir a la lista de contribuyentes
        else:
            # Devolver respuesta con errores
            return render(request, 'registroContribuyente.html', {'form1': form1, 'form2': form2, 'form3': form3})

    def get(self, request, *args, **kwargs):
        form1 = InformacionContribuyenteForm(prefix='informacion_contribuyente')
        form2 = DomicilioForm(prefix='domicilio')
        form3 = InformacionFiscalForm(prefix='informacion_fiscal')

        context = {
            'informacion_contribuyente_form': form1,
            'domicilio_form': form2,
            'informacion_fiscal_form': form3,
            'breadcrumb': {
                'parent': {'name': 'Contribuyente', 'url': '/contribuyente/home/'},
                'child': {'name': 'Registro de Nuevo Contribuyente', 'url': '/registro_contribuyente/'}
            },
            'editing': False,
            'sidebar': 'home_contribuyente'
        }

        return render(request, 'registroContribuyente.html', context)

class EditarContribuyenteView(View):

    def post(self, request, *args, **kwargs):
        # Cargar la instancia existente de Contribuyente usando el ID pasado en la URL
        contribuyente = get_object_or_404(Contribuyente, pk=kwargs['pk'])

        # Inicializar los formularios con la instancia del modelo y los datos POST
        form1 = InformacionContribuyenteForm(request.POST, request.FILES, instance=contribuyente, prefix='informacion_contribuyente')
        form2 = DomicilioForm(request.POST, request.FILES, instance=contribuyente, prefix='domicilio')
        form3 = InformacionFiscalFormUpdate(request.POST, request.FILES, instance=contribuyente, prefix='informacion_fiscal')

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            # Guardar la instancia del modelo con los datos de los formularios
            updated_contribuyente = form1.save(commit=False)
            form2.save(commit=False)
            form3.save(commit=False)

            # Manejar datos adicionales como la calle, colonia y municipio
            calle_id = request.POST.get('calle', '').strip()
            if calle_id:
                calle = Calle.objects.filter(id=calle_id).first()
                if calle:
                    updated_contribuyente.calle = calle
                    updated_contribuyente.colonia = calle.colonia
                    updated_contribuyente.municipio = calle.colonia.municipio

            updated_contribuyente.save()
            messages.success(request, 'Contribuyente actualizado con éxito')  # Agregar el mensaje de éxito

            return redirect('lista_ctr')  # Redirigir a la lista de contribuyentes
        else:
            # Devolver respuesta con errores
            return render(request, 'editarContribuyente.html', {'form1': form1, 'form2': form2, 'form3': form3})

    def get(self, request, *args, **kwargs):
        contribuyente = get_object_or_404(Contribuyente, pk=kwargs['pk'])
        form1 = InformacionContribuyenteForm(instance=contribuyente, prefix='informacion_contribuyente')
        form2 = DomicilioForm(instance=contribuyente, prefix='domicilio')
        form3 = InformacionFiscalFormUpdate(instance=contribuyente, prefix='informacion_fiscal')

        context = {
            'informacion_contribuyente_form': form1,
            'domicilio_form': form2,
            'informacion_fiscal_form': form3,
            'breadcrumb': {
                'parent': {'name': 'Registros De Contribuyentes', 'url': '/contribuyente/lista_contribuyentes/'},
                'child': {'name': 'Editar Contribuyente', 'url': '/editar_contribuyente/'}
            },
            'contribuyente': contribuyente,
            'sidebar': 'home_contribuyente',    
            'pdf_url': contribuyente.constancia_fiscal.url if contribuyente.constancia_fiscal else None

            }

        return render(request, 'editarContribuyente.html', context)