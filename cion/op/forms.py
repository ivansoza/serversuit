from django import forms
from .models import ODP, areas,Atendido,RevisionPropuesta
from django.contrib.auth import get_user_model

class ODPForm(forms.ModelForm):
    horas_asignadas = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'validationTooltip09',
            'placeholder': 'Horas asignadas',
        }),
        label='Horas asignadas'
    )

    class Meta:
        model = ODP
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.Municipio:
            municipio = user.Municipio
            # Filtra las áreas basadas en el municipio del usuario
            self.fields['areas'].queryset = areas.objects.filter(areasmunicipio__municipio=municipio)
        else:
            self.fields['areas'].queryset = areas.objects.none()

        self.fields['tipo_doc'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip01',
            'placeholder': 'Tipo de documento',
            'required': True
        })
        self.fields['procedencia'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip02',
            'placeholder': 'Ej. Apizaco',
            'required': True
        })
        self.fields['prioridad'].widget.attrs.update({
            'class': 'form-select',
            'id': 'validationTooltip03',
            'required': True
        })
        self.fields['dependencia'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip04',
            'placeholder': 'Ej. Presidencia',
            'required': True
        })
        self.fields['recibio'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip',
            'placeholder': 'Ej.Odp',
            'required': True
        })
        self.fields['observaciones'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip05',
            'placeholder': 'Observaciones'
        })
        self.fields['folio'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip06',
            'placeholder': 'Ej. 1323'
        })
        self.fields['archivo'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip07',
            'placeholder': 'Archivo adjunto',
            'required': False
        })
        self.fields['status'].widget.attrs.update({
            'class': 'form-check-input',
            'id': 'validationTooltip08'
        })
        self.fields['areas'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip010',
            'placeholder': 'Áreas',
            'required': True
        })

        # Mostrar el campo de horas solo si contestacion es True
        if self.instance.contestacion:
            self.fields['horas_asignadas'].required = False
        else:
            self.fields['horas_asignadas'].required = False

    def clean(self):
        cleaned_data = super().clean()
        contestacion = cleaned_data.get('contestacion')
        horas_asignadas = cleaned_data.get('horas_asignadas')

        if contestacion and horas_asignadas is None:
            self.add_error('horas_asignadas', 'Debes ingresar las horas asignadas si seleccionas la opción de contestación.')
        elif not contestacion and horas_asignadas is not None:
            self.add_error('horas_asignadas', 'No puedes ingresar horas asignadas si no seleccionas la opción de contestación.')
            
        for field_name in ['procedencia', 'dependencia', 'recibio', 'observaciones', 'folio']:
            value = cleaned_data.get(field_name)
            if value:
                cleaned_data[field_name] = value.upper()
                
        return cleaned_data



class AtendidoForm(forms.ModelForm):
    class Meta:
        model = Atendido
        fields = ['nombre', 'apellido', 'fecha', 'hora', 'archivo']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip02',
            'placeholder': 'Ej. Fernando',
            'required': True
        })
        self.fields['apellido'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip02',
            'placeholder': 'Ej. Mendieta',
            'required': True
        })
    
        self.fields['fecha'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip04',
            'placeholder': 'Ej. Presidencia',
            'required': True
        })
        self.fields['hora'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip04',
            'placeholder': 'Ej. Presidencia',
            'required': True
        })
        
        

from django import forms
from .models import RevisionPropuesta

class RevisionPropuestaForm(forms.ModelForm):
    class Meta:
        model = RevisionPropuesta
        fields = ['fecha', 'hora', 'acepta', 'noacepta', 'observaciones']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['fecha'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip04',
            'required': True
        })
        self.fields['hora'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip04',
            'required': True
        })
        self.fields['acepta'].widget.attrs.update({
            'class': 'form-check-input',
            'id': 'validationTooltip08'
        })
        self.fields['noacepta'].widget.attrs.update({
            'class': 'form-check-input',
            'id': 'validationTooltip08'
        })
        self.fields['observaciones'].widget.attrs.update({
            'class': 'form-control',
            'id': 'validationTooltip07',
            'placeholder': 'Observaciones'
        })
        
        if self.instance.noacepta:
            self.fields['observaciones'].required = False
        else:
            self.fields['observaciones'].required = True

    def clean(self):
        cleaned_data = super().clean()
        noacepta = cleaned_data.get('noacepta')
        observaciones = cleaned_data.get('observaciones')

        if noacepta and not observaciones:
            self.add_error('observaciones', 'Debes ingresar una descripción por el cual no aceptas la propuesta')
        elif not noacepta and observaciones:
            self.add_error('observaciones', 'No puedes ingresar una descripción si aceptas la respuesta.')
            
        return cleaned_data
