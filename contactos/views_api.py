from rest_framework import viewsets
from .models import Contacto
from .serializers import ContactoSerializer
from rest_framework.permissions import AllowAny

class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all().prefetch_related('telefonos')
    serializer_class = ContactoSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['email','nombre','apellido']
    search_fields = ['nombre','apellido','email','numeros__telefono']
