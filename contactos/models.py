from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r'^[0-9+\-\s()]{6,20}$', 'Ingrese un número de télefono válido.')

class Contacto(models.Model):
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre', 'apellido']

    def __str__(self):
        if self.email:
            return f"{self.nombre} {self.apellido} ({self.email})"
        else:
            return f"{self.nombre} {self.apellido}"

    def get_full_name(self):
        return f"{self.nombre} {self.apellido}".strip()

class Telefono(models.Model):
    contacto = models.ForeignKey(Contacto, related_name='telefonos', on_delete=models.CASCADE)
    numero_telefono = models.CharField(max_length=30, validators=[phone_validator])
    referencia = models.CharField(max_length=30, default='móvil', blank=True)

    def __str__(self):
        return f"{self.numero_telefono} ({self.referencia})"
