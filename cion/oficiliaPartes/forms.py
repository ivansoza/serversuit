from django import forms
from .models import recepcionDocumentos, respuesta
from catalogos.models import  areasMunicipio, areas

class recepcionDocumentosForms(forms.ModelForm):
    class Meta:
        model = recepcionDocumentos
        fields = [
            'folio_odp', 'areas', 'recibio', 'tipo_doc', 'prioridad', 'dependencia', 
            'procedencia', 'folio_expediente', 'archivo', 'contestacion', 'horas_asignadas', 
            'observaciones'
        ]
        widgets = {
            'folio_odp': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationFolio_odp',
                'placeholder': 'Ingrese un folio',
            }),
            'areas': forms.Select(attrs={
                'class': 'form-select',
                'id': 'validationAreas',
                'placeholder': 'Seleccione un área',
                'required': 'required',
            }),
            'recibio': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationRecibio',
                'placeholder': 'Ingrese el nombre completo de quien recibe',
                'required': 'required',
            }),
            'tipo_doc': forms.Select(attrs={
                'class': 'form-select',
                'id': 'validationTipoDoc',
                'placeholder': 'Seleccione un tipo de documento',
                'required': 'required',
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select',
                'id': 'validationPrioridad',
                'placeholder': 'Seleccione un tipo de prioridad',
                'required': 'required',
            }),
            'dependencia': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationDependencia',
                'placeholder': 'Ingrese la dependencia',
                'required': 'required',
            }),
            'procedencia': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationProcedencia',
                'placeholder': 'Ingrese la procedencia',
                'required': 'required',
            }),
            'folio_expediente': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationFolioExpediente',
                'placeholder': 'Ingrese el folio o expediente',
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'validationArchivo',
            }),
            'contestacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'validationContestacion',
            }),
            'horas_asignadas': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'validationHorasAsignadas',
                'placeholder': 'Ingrese las horas asignadas',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'validationObservaciones',
                'placeholder': 'Ingrese observaciones',
                'rows': 2,
            }),
        }
    def __init__(self, *args, **kwargs):
        municipio = kwargs.pop('municipio', None)
        super(recepcionDocumentosForms, self).__init__(*args, **kwargs)
        if municipio:
            # Filtrar las áreas basándose en areasMunicipio
            areas_municipio = areasMunicipio.objects.filter(municipio=municipio)
            areas_ids = areas_municipio.values_list('area', flat=True)
            self.fields['areas'].queryset = areas.objects.filter(id__in=areas_ids)

class respuestaForms(forms.ModelForm):
    class Meta:
        model = respuesta
        fields = ['odp','usuario','archivo','observaciones']
        widgets = {
            'odp': forms.Select(attrs={
                'class': 'form-select',
                'id': 'validationODP',
                'placeholder': 'Seleccione una llave',
                'required': 'required',
            }),
            'usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationUsuario',
                'placeholder': 'Ingrese el nombre completo de quien contesta',
                'required': 'required',
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'validationArchivo',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'validationObservaciones',
                'placeholder': 'Ingrese observaciones',
                'rows': 2,
            }),
        }
