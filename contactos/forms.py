from django import forms
from django.forms import inlineformset_factory
from .models import Contacto, Telefono

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'apellido', 'email']

TelefonoFormSet = inlineformset_factory(
    Contacto, Telefono, fields=('numero_telefono','referencia'), extra=1, min_num=1, validate_min=True, can_delete=True
)
