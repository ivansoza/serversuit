from django import forms
from .models import noServicio

class noServicioForm(forms.ModelForm):
    class Meta:
        model = noServicio
        fields = [
            'rfc', 'homoclave', 'curp', 'nombre', 'ApellidoP', 'ApellidoM', 'email', 'telefono',
            'nombre_mc', 'ApellidoP_mc', 'ApellidoM_mc', 'claveCatastral',
            'noServicio', 'tipoServicio', 'municipio', 'registro', 'contri', 'predio', 'razonSocial',
            'tipoPersona', 'estado', 'codigo_postal', 'municipio_predio', 'colonia', 'calle', 'numero_exterior', 'numero_interior',
            'superficie_total', 'superficie_construida', 'uso_predio', 'valor_catastral'
        ]
        widgets = {
            'rfc': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationRFC',
                'placeholder': 'Ingresa tu RFC',
                'required': 'required',
            }),
            'homoclave': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationHomoclave',
                'placeholder': 'Ingresa tu homoclave',
                'readonly': 'readonly'
            }),
            'curp': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationCurp',
                'placeholder': 'Ingresa tu CURP',
                'required': 'required',
                'readonly': 'readonly'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationNombre',
                'placeholder': 'Ingresa tu nombre',
                'required': 'required',
                'readonly': 'readonly'
            }),
            'ApellidoP': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationApellidoP',
                'placeholder': 'Ingresa tu apellido paterno',
                'required': 'required',
                'readonly': 'readonly'
            }),
            'ApellidoM': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationApellidoM',
                'placeholder': 'Ingresa tu apellido materno',
                'required': 'required',
                'readonly': 'readonly'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationEmail',
                'placeholder': 'ejemplo@correo.com',
                'required': 'required',
                'readonly': 'readonly'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationTelefono',
                'placeholder': 'Ingresa tu teléfono',
                'required': 'required',
                'readonly': 'readonly'
            }),
            'nombre_mc': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationNombreMC',
                'placeholder': 'Ingresa tu nombre',
                'readonly': 'readonly'
            }),
            'ApellidoP_mc': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationApellidoPMC',
                'placeholder': 'Ingresa tu apellido paterno',
                'readonly': 'readonly'
            }),
            'ApellidoM_mc': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationApellidoMMC',
                'placeholder': 'Ingresa tu apellido materno',
                'readonly': 'readonly'
            }),
            'claveCatastral': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationClaveCatastral',
                'placeholder': 'Ingresa la clave catastral',
            }),
            'noServicio': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationNoServicio',
                'placeholder': 'Ingresa el número de servicio',
                'required': 'required',
            }),
            'tipoServicio': forms.Select(attrs={
                'class': 'form-select',
                'id': 'validationTipoServicio',
                'required': 'required',
            }),
            'municipio': forms.Select(attrs={
                'class': 'form-select readonly-select',
                'id': 'validationMunicipio',
                'readonly': 'readonly'
            }),
            'registro': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationRegistro',
                'placeholder': 'Ingresa el nombre de quien lo registró',
                'required': 'required',
                'readonly': 'readonly'
            }),
            'contri': forms.Select(attrs={
                'class': 'form-select',
                'id': 'validationContribuyente',
                'required': 'required',
            }),
            'predio': forms.Select(attrs={
                'class': 'form-select readonly-select',
                'id': 'validationPredio',
                'readonly': 'readonly'
            }),
            'razonSocial': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationRazonSocial',
                'placeholder': 'Ingresa la razón social',
                'readonly': 'readonly'
            }),
            'tipoPersona': forms.Select(attrs={
                'class': 'form-select readonly-select',
                'id': 'validationTipoPersona',
                'required': 'required',
                'readonly': 'readonly'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationEstado',
                'placeholder': 'Ingresa el estado',
                'readonly': 'readonly'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationCodigoPostal',
                'placeholder': 'Ingresa el código postal',
                'readonly': 'readonly'
            }),
            'municipio_predio': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationMunicipioP',
                'placeholder': 'Ingresa el municipio',
                'readonly': 'readonly'
            }),
            'colonia': forms.Select(attrs={
                'class': 'form-select readonly-select',
                'id': 'validationColonia',
                'readonly': 'readonly'
            }),
            'calle': forms.Select(attrs={
                'class': 'form-select readonly-select',
                'id': 'validationCalle',
                'readonly': 'readonly'
            }),
            'numero_exterior': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationNumeroExterior',
                'placeholder': 'Ingresa el número exterior',
                'readonly': 'readonly'
            }),
            'numero_interior': forms.TextInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationNumeroInterior',
                'placeholder': 'Ingresa el número interior',
                'readonly': 'readonly'
            }),
            'superficie_total': forms.NumberInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationSuperficieTotal',
                'placeholder': 'Ingresa la superficie total',
                'readonly': 'readonly'
            }),
            'superficie_construida': forms.NumberInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationSuperficieConstruida',
                'placeholder': 'Ingresa la superficie construida',
                'readonly': 'readonly'
            }),
            'uso_predio': forms.Select(attrs={
                'class': 'form-select readonly-select',
                'id': 'validationUsoPredio',
                'readonly': 'readonly'
            }),
            'valor_catastral': forms.NumberInput(attrs={
                'class': 'form-control readonly-style',
                'id': 'validationValorCatastral',
                'placeholder': 'Ingresa el valor catastral',
                'readonly': 'readonly'
            })
        }
