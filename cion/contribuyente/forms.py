from django import forms

from contribuyente.models import Contribuyente
from django.core.exceptions import ValidationError

class InformacionContribuyenteForm(forms.ModelForm):
    class Meta:
        model = Contribuyente
        fields = ['tipoPersona', 'curp', 'nombre', 'razonSocial', 'apellidoP', 'apellidoM', 'email', 'telefono', 'mc', 'nombre_mc', 'apellidoP_mc', 'apellidoM_mc']
        widgets = {
            'tipoPersona': forms.Select(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su CURP'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'razonSocial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la razón social'}),
            'apellidoP': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido paterno'}),
            'apellidoM': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido materno'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de teléfono'}),
            'mc': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nombre_mc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'apellidoP_mc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido paterno'}),
            'apellidoM_mc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido materno'}),
        }
        labels = {
            'tipoPersona': 'Tipo de persona',
            'curp': 'CURP',
            'nombre': 'Nombre (s)',
            'razonSocial': 'Razon social',
            'apellidoP': 'Apellido paterno',
            'apellidoM': 'Apellido materno',
            'email': 'Correo electrónico',
            'telefono': 'No. teléfono',
            'mc': 'Marcar, Si desea agregar un nombre adicional',
            'nombre_mc': 'Nombre (s)',
            'apellidoP_mc': 'Apellido paterno',
            'apellidoM_mc': 'Apellido materno'
        }
class DomicilioForm(forms.ModelForm):
    class Meta:
        model = Contribuyente  # Asegúrate de que este es el modelo correcto
        fields = ['numeroE', 'numeroI']
        widgets = {
         
            'numeroE': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número exterior'}),
            'numeroI': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número interior'}),
     
        }
        labels = {
            'numeroE': 'No. exterior',
            'numeroI': 'No. interior',
        }


class InformacionFiscalForm(forms.ModelForm):
    class Meta:
        model = Contribuyente  # Verifica que este es el modelo correcto
        fields = ['rfc', 'homoclave', 'constancia_fiscal']
        widgets = {
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su RFC'}),
            'homoclave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su homoclave'}),
            'constancia_fiscal': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
        }
        labels = {
            'rfc': 'RFC',
            'homoclave': 'Homoclave',
            'constancia_fiscal': 'Constancia de situación fiscal'
        }

    def clean_constancia_fiscal(self):
        constancia_fiscal = self.cleaned_data.get('constancia_fiscal')
        if constancia_fiscal:
            if not constancia_fiscal.name.endswith('.pdf'):
                raise forms.ValidationError('El archivo debe estar en formato PDF.')
        return constancia_fiscal
    
class InformacionFiscalFormUpdate(forms.ModelForm):
    class Meta:
        model = Contribuyente  # Verifica que este es el modelo correcto
        fields = ['rfc', 'homoclave', 'constancia_fiscal']
        widgets = {
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su RFC'}),
            'homoclave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su homoclave'}),
            'constancia_fiscal': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),


        }
        labels = {
            'rfc': 'RFC',
            'homoclave': 'Homoclave',
            'constancia_fiscal': 'Constancia de situación fiscal'
        }
    def clean_constancia_fiscal(self):
        constancia_fiscal = self.cleaned_data.get('constancia_fiscal')
        if constancia_fiscal and hasattr(constancia_fiscal, 'file'):
            # Verifica si es un archivo nuevo que está siendo cargado
            if hasattr(constancia_fiscal.file, 'content_type'):
                if not constancia_fiscal.file.content_type == 'application/pdf':
                    raise forms.ValidationError('Solo se permiten archivos PDF.')
            return constancia_fiscal
        else:
            # Si no es un archivo nuevo, simplemente retorna el valor sin validar el content_type
            return constancia_fiscal