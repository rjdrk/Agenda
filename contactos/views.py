from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Contacto
from .forms import ContactoForm, TelefonoFormSet

class ContactoListView(ListView):
    model = Contacto
    template_name = 'contactos/contacto_list.html'
    paginate_by = 20
    context_object_name = 'contacto'

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        qs = super().get_queryset().prefetch_related('telefonos')
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(apellido__icontains=q) |
                Q(email__icontains=q) |
                Q(telefonos__numero_telefono__icontains=q)
            ).distinct()
        return qs

def contacto_create(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        formset = TelefonoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            contacto = form.save()
            formset.instance = contacto
            formset.save()
            return redirect('contactos:contacto_list')
    else:
        form = ContactoForm()
        formset = TelefonoFormSet()
    return render(request, 'contactos/contacto_form.html', {'form': form, 'formset': formset, 'create': True})

def contacto_edit(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        formset = TelefonoFormSet(request.POST, instance=contacto)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('contactos:contacto_list')
    else:
        form = ContactoForm(instance=contacto)
        formset = TelefonoFormSet(instance=contacto)
    return render(request, 'contactos/contacto_form.html', {'form': form, 'formset': formset, 'create': False})

class ContactoDeleteView(DeleteView):
    model = Contacto
    template_name = 'contactos/contacto_confirm_delete.html'
    success_url = reverse_lazy('contactos:contacto_list')
