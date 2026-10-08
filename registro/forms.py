from django import forms
from .models import Alerta, Parada


class AlertaForm(forms.ModelForm):

    class Meta:
        model = Alerta
        fields = ['maquina', 'descripcion']

        widgets = {
            'maquina': forms.TextInput(attrs={
                'placeholder': 'Ej: Empacadora 1'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describe la alerta'
            }),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '')

        if not descripcion.strip():
            raise forms.ValidationError(
                'La descripción no puede estar vacía.'
            )

        return descripcion


class ParadaForm(forms.ModelForm):

    class Meta:
        model = Parada
        fields = ['maquina', 'inicio', 'fin', 'motivo']

        widgets = {
            'maquina': forms.TextInput(attrs={
                'placeholder': 'Ej: Empacadora 1'
            }),
            'inicio': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'fin': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'motivo': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Motivo de la parada'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['inicio'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]

        self.fields['fin'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo', '')

        if not motivo.strip():
            raise forms.ValidationError(
                'El motivo no puede estar vacío.'
            )

        return motivo

    def clean(self):
        cleaned_data = super().clean()

        inicio = cleaned_data.get('inicio')
        fin = cleaned_data.get('fin')

        if inicio and fin and fin <= inicio:
            self.add_error(
                'fin',
                'La fecha y hora de finalización debe ser posterior '
                'a la fecha y hora de inicio.'
            )

        return cleaned_data