from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Incidencia
from .forms import IncidenciaForm


class IncidenciaListView(ListView):
    model = Incidencia
    template_name = 'incidencias/lista_incidencias.html'
    context_object_name = 'incidencias'
    ordering = ['-fecha_creacion']


class IncidenciaCreateView(CreateView):
    model = Incidencia
    form_class = IncidenciaForm
    template_name = 'incidencias/crear_incidencia.html'
    success_url = reverse_lazy('lista_incidencias')
