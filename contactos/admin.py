from django.contrib import admin
from .models import Contacto, Telefono

class TelefonoInline(admin.TabularInline):
    model = Telefono
    extra = 0

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellido','email')
    inlines = [TelefonoInline]
