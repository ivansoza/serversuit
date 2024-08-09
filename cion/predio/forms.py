
from django import forms

from catalogos.models import Calle, Municipio

from .models import predio


class PredioForm(forms.ModelForm):
    class Meta:
        model = predio
        fields = [
            'contribuyente', 'clave_catastral', 'numero_exterior', 'numero_interior', 'superficie_total', 
            'superficie_construida', 'uso_predio', 'valor_catastral',  'curp', 'rfc', 'homoclave','nombre','ApellidoP','ApellidoM','nombre_mc','ApellidoP_mc','ApellidoM_mc','razonSocial','email','telefono'
        ]
        widgets = {
            'clave_catastral': forms.TextInput(attrs={'id': 'id_clave_catastral', 'class': 'form-control', 'placeholder': 'Ingrese la clave catastral'}),
            'numero_exterior': forms.TextInput(attrs={'id': 'id_numero_exterior', 'class': 'form-control', 'placeholder': 'Número exterior'}),
            'numero_interior': forms.TextInput(attrs={'id': 'id_numero_interior', 'class': 'form-control', 'placeholder': 'Número interior'}),
            'superficie_total': forms.NumberInput(attrs={'id': 'id_superficie_total', 'class': 'form-control', 'placeholder': 'Superficie total'}),
            'superficie_construida': forms.NumberInput(attrs={'id': 'id_superficie_construida', 'class': 'form-control', 'placeholder': 'Superficie construida'}),
            'valor_catastral': forms.NumberInput(attrs={'id': 'id_valor_catastral', 'class': 'form-control', 'placeholder': 'Valor catastral'}),
            'uso_predio': forms.Select(attrs={'placeholder': 'Seleccione el tipo de predio'}),

            'contribuyente': forms.Select(attrs={'id': 'id_contribuyente', 'class': 'form-select'}),
            'curp': forms.TextInput(attrs={'id': 'id_curp', 'class': 'form-control', 'placeholder': 'Ingrese el CURP'}),
            'rfc': forms.TextInput(attrs={'id': 'id_rfc', 'class': 'form-control', 'maxlength': '10', 'placeholder': 'Ingrese el RFC sin homoclave'}),
            'homoclave': forms.TextInput(attrs={'id': 'id_homoclave', 'class': 'form-control', 'maxlength': '3', 'placeholder': 'Ingrese la homoclave'}),
                        # Nuevos campos
            'nombre': forms.TextInput(attrs={'id': 'id_nombre', 'class': 'form-control', 'placeholder': 'Ingrese el nombre'}),
            'ApellidoP': forms.TextInput(attrs={'id': 'id_ApellidoP', 'class': 'form-control', 'placeholder': 'Ingrese el apellido paterno'}),
            'ApellidoM': forms.TextInput(attrs={'id': 'id_ApellidoM', 'class': 'form-control', 'placeholder': 'Ingrese el apellido materno'}),
            'nombre_mc': forms.TextInput(attrs={'id': 'id_nombre_mc', 'class': 'form-control', 'placeholder': 'Ingrese el nombre del medio de contacto'}),
            'ApellidoP_mc': forms.TextInput(attrs={'id': 'id_ApellidoP_mc', 'class': 'form-control', 'placeholder': 'Ingrese el apellido paterno del medio de contacto'}),
            'ApellidoM_mc': forms.TextInput(attrs={'id': 'id_ApellidoM_mc', 'class': 'form-control', 'placeholder': 'Ingrese el apellido materno del segundo nombre'}),
            'razonSocial': forms.TextInput(attrs={'id': 'id_RazonSocial', 'class': 'form-control', 'placeholder': 'Ingrese el Nombre de la Razón Social'}),
            'email': forms.EmailInput(attrs={'id': 'id_email', 'class': 'form-control', 'placeholder': 'Ingrese el email'}),
            'telefono': forms.TextInput(attrs={'id': 'id_telefono', 'class': 'form-control', 'placeholder': 'Ingrese el teléfono'}),


        }
    def __init__(self, *args, **kwargs):
        super(PredioForm, self).__init__(*args, **kwargs)
                # Hacer todos los campos no obligatorios
        for field in self.fields:
            self.fields[field].required = False
        self.fields['curp'].label = "CURP"

        self.fields['clave_catastral'].required = True
        self.fields['uso_predio'].required = True
        self.fields['rfc'].label = "RFC"
        self.fields['razonSocial'].label = "Razón social"
        self.fields['nombre'].label = "Nombre(s)"
        self.fields['ApellidoP'].label = "Apellido paterno"
        self.fields['ApellidoM'].label = "Apellido materno"
        self.fields['nombre_mc'].label = "Nombre(s)"
        self.fields['ApellidoP_mc'].label = "Apellido paterno"
        self.fields['ApellidoM_mc'].label = "Apellido materno"
        self.fields['superficie_total'].label = "Superficie total (m²)"
        self.fields['superficie_construida'].label = "Superficie construida (m²)"
        # Asegurarse que el campo 'uso_predio'
        self.fields['uso_predio'].choices = [('','Seleccione el tipo de predio')] + list(predio.USO_PREDIO_CHOICES)




class PredioFormUpdate(forms.ModelForm):
    class Meta:
        model = predio
        fields = [
            'contribuyente', 'clave_catastral', 'numero_exterior', 'numero_interior', 'superficie_total', 
            'superficie_construida', 'uso_predio', 'valor_catastral',  'curp', 'rfc', 'homoclave','nombre','ApellidoP','ApellidoM','nombre_mc','ApellidoP_mc','ApellidoM_mc','razonSocial','email','telefono'
        ]
        widgets = {
            'clave_catastral': forms.TextInput(attrs={'id': 'id_clave_catastral', 'class': 'form-control', 'placeholder': 'Ingrese la clave catastral'}),
            'numero_exterior': forms.TextInput(attrs={'id': 'id_numero_exterior', 'class': 'form-control', 'placeholder': 'Número exterior'}),
            'numero_interior': forms.TextInput(attrs={'id': 'id_numero_interior', 'class': 'form-control', 'placeholder': 'Número interior'}),
            'superficie_total': forms.NumberInput(attrs={'id': 'id_superficie_total', 'class': 'form-control', 'placeholder': 'Superficie total'}),
            'superficie_construida': forms.NumberInput(attrs={'id': 'id_superficie_construida', 'class': 'form-control', 'placeholder': 'Superficie construida'}),
            'valor_catastral': forms.NumberInput(attrs={'id': 'id_valor_catastral', 'class': 'form-control', 'placeholder': 'Valor catastral'}),
            'uso_predio': forms.Select(attrs={'placeholder': 'Seleccione el tipo de predio'}),

            'contribuyente': forms.Select(attrs={'id': 'id_contribuyente', 'class': 'form-select'}),
            'curp': forms.TextInput(attrs={'id': 'id_curp', 'class': 'form-control', 'placeholder': 'Ingrese el CURP'}),
            'rfc': forms.TextInput(attrs={'id': 'id_rfc', 'class': 'form-control', 'maxlength': '10', 'placeholder': 'Ingrese el RFC sin homoclave'}),
            'homoclave': forms.TextInput(attrs={'id': 'id_homoclave', 'class': 'form-control', 'maxlength': '3', 'placeholder': 'Ingrese la homoclave'}),
                        # Nuevos campos
            'nombre': forms.TextInput(attrs={'id': 'id_nombre', 'class': 'form-control', 'placeholder': 'Ingrese el nombre'}),
            'ApellidoP': forms.TextInput(attrs={'id': 'id_ApellidoP', 'class': 'form-control', 'placeholder': 'Ingrese el apellido paterno'}),
            'ApellidoM': forms.TextInput(attrs={'id': 'id_ApellidoM', 'class': 'form-control', 'placeholder': 'Ingrese el apellido materno'}),
            'nombre_mc': forms.TextInput(attrs={'id': 'id_nombre_mc', 'class': 'form-control', 'placeholder': 'Ingrese el nombre del medio de contacto'}),
            'ApellidoP_mc': forms.TextInput(attrs={'id': 'id_ApellidoP_mc', 'class': 'form-control', 'placeholder': 'Ingrese el apellido paterno del medio de contacto'}),
            'ApellidoM_mc': forms.TextInput(attrs={'id': 'id_ApellidoM_mc', 'class': 'form-control', 'placeholder': 'Ingrese el apellido materno del segundo nombre'}),
            'razonSocial': forms.TextInput(attrs={'id': 'id_RazonSocial', 'class': 'form-control', 'placeholder': 'Ingrese el Nombre de la Razón Social'}),
            'email': forms.EmailInput(attrs={'id': 'id_email', 'class': 'form-control', 'placeholder': 'Ingrese el email'}),
            'telefono': forms.TextInput(attrs={'id': 'id_telefono', 'class': 'form-control', 'placeholder': 'Ingrese el teléfono'}),


        }
    def __init__(self, *args, **kwargs):
        super(PredioFormUpdate, self).__init__(*args, **kwargs)
                # Hacer todos los campos no obligatorios
        for field in self.fields:
            self.fields[field].required = False
        # Configurar campos específicos como solo lectura si tienen valores al inicializar
        readonly_fields = ['contribuyente', 'rfc', 'homoclave', 'curp', 'nombre', 'ApellidoP', 'ApellidoM', 'razonSocial', 'email', 'telefono', 'nombre_mc', 'ApellidoP_mc', 'ApellidoM_mc']
        instance = kwargs.get('instance', None)
        if instance:
            for field_name in readonly_fields:
                if getattr(instance, field_name, None):
                    self.fields[field_name].widget.attrs['readonly'] = True
                    self.fields[field_name].widget.attrs['class'] = 'form-control readonly-style'

        self.fields['curp'].label = "CURP"
        self.fields['clave_catastral'].required = True
        self.fields['uso_predio'].required = True
        self.fields['rfc'].label = "RFC"
        self.fields['razonSocial'].label = "Razón social"
        self.fields['nombre'].label = "Nombre(s)"
        self.fields['ApellidoP'].label = "Apellido paterno"
        self.fields['ApellidoM'].label = "Apellido materno"
        self.fields['nombre_mc'].label = "Nombre(s)"
        self.fields['ApellidoP_mc'].label = "Apellido paterno"
        self.fields['ApellidoM_mc'].label = "Apellido materno"
        self.fields['superficie_total'].label = "Superficie total (m²)"
        self.fields['superficie_construida'].label = "Superficie construida (m²)"
        # Asegurarse que el campo 'uso_predio'
        self.fields['uso_predio'].choices = [('','Seleccione el tipo de predio')] + list(predio.USO_PREDIO_CHOICES)



