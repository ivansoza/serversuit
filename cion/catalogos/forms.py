from django import forms

from cionapp.models import PaginaInicio
from .models import Descuentos,Recargos, areasMunicipio,areas, ServicioMunicipio, Servicios
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import CustomUser
from .models import Municipio, areasMunicipio, areas
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        # Eliminar el atributo autofocus de los tres campos
        self.fields['old_password'].widget.attrs.pop('autofocus', None)
        self.fields['new_password1'].widget.attrs.pop('autofocus', None)
        self.fields['new_password2'].widget.attrs.pop('autofocus', None)
        
        # Eliminar el texto de ayuda de new_password1 y new_password2
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None

class descuentoRecargoForm(forms.ModelForm):
    class Meta:
        model = Descuentos
        fields = ['tipo','nombre', 'monto_descuento','municipio', 'estatus_descuento']
        widgets = {
            'tipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descuento',
                'required': 'required'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del descuento',
                'required': 'required'
            }),
            'monto_descuento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monto de descuento',
            }),
            'municipio': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el municipio',
                'required': 'required'
            }),
            'estatus_descuento': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el estatus',
                'required': 'required'
            }),
        }
class recargoForm(forms.ModelForm):
    class Meta:
        model = Recargos
        fields = ['tipo','nombre', 'monto_recargo','municipio','estatus_recargos']
        widgets = {
            'tipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Recargo',
                'required': 'required'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del recargo',
                'required': 'required'
            }),
            'monto_recargo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monto de recargo',
            }),
            'municipio': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el municipio',
                'required': 'required'
            }),
            'estatus_recargos': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el estatus',
                'required': 'required'
            }),
        }

class AreasMunicipioForm(forms.ModelForm):
    class Meta:
        model = areasMunicipio
        fields = ['area', 'municipio']
        widgets = {
            'area': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
            'municipio': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        municipio_usuario = kwargs.pop('municipio_usuario', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar las áreas visibles para el municipio del usuario o generales
        areas_visibles = areas.obtener_areas_visibles(municipio_usuario)
        self.fields['area'].queryset = areas_visibles

class AreasForms(forms.ModelForm):
    class Meta:
        model = areas
        fields = ['Area', 'municipios_visibles']
        widgets = {
            'municipios_visibles': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione el municipio',
                'required': 'required'
            }),
            'Area': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la área',
                'required': 'required'
            }),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'apellido_materno', 'sexo','areas','es_responsable')

    def __init__(self, *args, **kwargs):
        municipio = kwargs.pop('municipio', None)

        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['sexo'].choices = [('','Selecciona un sexo')] + list(CustomUser.SEXO_CHOICES) # Añade la opción inicial
        self.fields['username'].widget.attrs.update({'placeholder': 'Nombre de Usuario'})

        # Asegurando que los campos de nombre y apellidos sean requeridos
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['sexo'].required = True

        self.fields['username'].help_text = '' 
        self.fields['username'].label = 'Nombre de Usuario'
        # Configuración para el campo 'email'
        self.fields['email'].widget.attrs.update({'placeholder': 'Correo Electrónico'})
        self.fields['email'].label = 'Correo Electrónico'
        # Configuración para el campo 'first_name'
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Nombre(s)'})
        self.fields['first_name'].label = 'Nombre(s)'

        # Configuración para el campo 'last_name'
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Apellido Paterno'})
        self.fields['last_name'].label = 'Apellido Paterno'
        self.fields['apellido_materno'].widget.attrs.update({'placeholder': 'Apellido Materno'})
        self.fields['apellido_materno'].label = 'Apellido Materno'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
         # Configuraciones para los campos de contraseña
        self.fields['password1'].widget.attrs.update({'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmar contraseña'})

        if municipio:
            areas_queryset = areas.objects.filter(areasmunicipio__municipio=municipio)
            self.fields['areas'].queryset = areas_queryset
        else:
            self.fields['areas'].queryset = areas.objects.none()
        self.fields['areas'].widget.attrs['class'] = 'select2'
        self.fields['areas'].label = 'Áreas'
        self.fields['areas'].required = True

class ServicioMunicipioForms(forms.ModelForm):
    class Meta:
        model = ServicioMunicipio
        fields = ['clave', 'municipio', 'concepto', 'monto', 'area']
        widgets = {
            'clave': forms.Select(attrs={'class': 'form-control select2'}),  # Agregada la clase select2 aquí
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        municipio_usuario = kwargs.pop('municipio_usuario', None)
        super(ServicioMunicipioForms, self).__init__(*args, **kwargs)
        if municipio_usuario:
            # Filtrar las áreas basándose en areasMunicipio
            areas_municipio = areasMunicipio.objects.filter(municipio=municipio_usuario)
            areas_ids = areas_municipio.values_list('area', flat=True)
            self.fields['area'].queryset = areas.objects.filter(id__in=areas_ids)


class ServiciosForms(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = ['codigoServicio', 'descripcion','claveProducto','fecha_inicio','fecha_fin','estatus']
        widgets = {
            'codigoServicio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de servicio',
                'required': 'required'
            }),
             'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción',
                'required': 'required'
            }),
            'claveProducto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Clave Producto',
                'required': 'required'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # Esto especifica que el input es de tipo fecha
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'estatus': forms.Select(attrs={
                'class': 'form-control',
            }),
           
        }

class PaginaInicioForm(forms.ModelForm):
    class Meta:
        model = PaginaInicio
        fields = ['titulo','mapa_html', 'mision', 'vision', 'telefono', 'email', 'direccion']
        labels = {
            'titulo': 'Identificación de la Organización',
            'mision': 'Misión de la Organización',
            'vision': 'Visión de la Organización',
            'telefono': 'Teléfono de Contacto',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección Física',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: H. Ayuntamiento (nombre de la organización)', 'required': False}),
            'mapa_html': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': 'Ingrese el código HTML para el mapa', 'required': False}),
            'mision': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': 'Describa la misión', 'required': False}),
            'vision': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': 'Describa la visión', 'required': False}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: +1 234 567 8900', 'required': False}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: correo@example.com', 'required': False}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección completa', 'required': False}),
        }
        

