from django import forms
from django.core.exceptions import ValidationError
import os
from .models import ToxicPattern


class TextAnalysisForm(forms.Form):
    """
    Formulario para análisis de texto.
    """

    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Ingresa el texto que deseas analizar...',
            'maxlength': 10000
        }),
        label='Texto a analizar',
        help_text='Máximo 10,000 caracteres',
        max_length=10000,
        required=False
    )

    document = forms.FileField(
        required=False,
        label='Adjuntar archivo',
        help_text='Formatos permitidos: .pdf, .txt, .html',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.txt,.html,.htm'
        })
    )

    def clean(self):
        """
        Validación personalizada para asegurar que exista texto o archivo.
        """
        cleaned_data = super().clean()
        text = (cleaned_data.get('text') or '').strip()
        document = cleaned_data.get('document')

        if not text and not document:
            raise ValidationError('Debes ingresar texto o adjuntar un archivo para analizar.')

        if document:
            ext = os.path.splitext(document.name)[1].lower()
            if ext not in {'.pdf', '.txt', '.html', '.htm'}:
                raise ValidationError('Formato de archivo no soportado. Usa .pdf, .txt o .html.')

            if document.size > 5 * 1024 * 1024:  # 5 MB
                raise ValidationError('El archivo es demasiado grande (máximo 5 MB).')

        cleaned_data['text'] = text
        return cleaned_data


class ToxicPatternForm(forms.ModelForm):
    """
    Formulario para crear/editar patrones tóxicos personalizados.
    """

    class Meta:
        model = ToxicPattern
        fields = ['name', 'pattern', 'toxicity_type', 'toxicity_level', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre descriptivo del patrón'
            }),
            'pattern': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Expresión regular (ej: \\b(palabra1|palabra2)\\b)'
            }),
            'toxicity_type': forms.Select(attrs={'class': 'form-control'}),
            'toxicity_level': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción opcional del patrón'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean_pattern(self):
        """
        Valida que el patrón regex sea válido.
        """
        pattern = self.cleaned_data.get('pattern', '').strip()

        if not pattern:
            raise ValidationError('El patrón no puede estar vacío.')

        try:
            import re
            re.compile(pattern)
        except re.error as e:
            raise ValidationError(f'Patrón regex inválido: {str(e)}')

        return pattern

    def clean_name(self):
        """
        Valida que el nombre sea único.
        """
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise ValidationError('El nombre no puede estar vacío.')

        # Verificar unicidad (excluyendo la instancia actual si estamos editando)
        queryset = ToxicPattern.objects.filter(name=name)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError('Ya existe un patrón con este nombre.')

        return name
