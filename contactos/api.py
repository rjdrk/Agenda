from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ContactoViewSet

router = DefaultRouter()
router.register(r'contacto', ContactoViewSet, basename='contacto')

urlpatterns = [
    path('', include(router.urls)),
]
