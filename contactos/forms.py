from django import forms
from django.forms import inlineformset_factory
from .models import Contacto, Telefono

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'apellido', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el email (opcional)'
            }),
        }
        labels = {
            'nombre': 'Nombre *',
            'apellido': 'Apellido *',
            'email': 'Email',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido', '')
        email = cleaned_data.get('email', '')

        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')

        if self.instance.pk is None:
            existing = Contacto.objects.filter(
                nombre__iexact=nombre,
                apellido__iexact=apellido,
                email__iexact=email if email else ''
            )
            if existing.exists() and email:
                self.add_error('email', 'Ya existe un contacto con este nombre y email.')

        return cleaned_data

TelefonoFormSet = inlineformset_factory(
    Contacto,
    Telefono, 
    fields=('numero_telefono','referencia'), 
    extra=0, 
    min_num=1, 
    validate_min=True, 
    can_delete=True,
    widgets={
        'numero_telefono': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: +502 1234-5678'
        }),
        'referencia': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: móvil, casa, trabajo'
        }),
    }
)
