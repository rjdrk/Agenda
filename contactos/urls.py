from django.urls import path
from . import views

app_name = 'contactos'

urlpatterns = [
    path('', views.ContactoListView.as_view(), name='contacto_list'),
    path('contacto/add/', views.contacto_create, name='contacto_add'),
    path('contacto/<int:pk>/edit/', views.contacto_edit, name='contacto_edit'),
    path('contacto/<int:pk>/delete/', views.ContactoDeleteView.as_view(), name='contacto_delete'),
]
