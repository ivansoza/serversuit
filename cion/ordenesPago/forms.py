from django import forms

from .models import estadoNoServicio, estadoPredio

class estadoNoServicioForms(forms.ModelForm):
    meses_seleccionados = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = estadoNoServicio
        fields = ['noServicio', 'anio','mes', 'monto']
        widgets = {
            'noServicio': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona el numero de servicio',
                'required': 'required'
            }),
            'anio': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Año',
                'required': 'required'

            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monto',
                'required': 'required'

            }),
        }

class estadoPredioForms(forms.ModelForm):
    class Meta:
        model = estadoPredio
        fields =['claveCatastarl','anio', 'monto']
        widgets = {
            'claveCatastarl': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona la clave catastral',
                'required': 'required'
            }),
            'anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Año',
                'required': 'required'

            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monto',
                'required': 'required'

            }),
        }