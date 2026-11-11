from django.urls import path
from .views import IncidenciaListView, IncidenciaCreateView

urlpatterns = [
    path('', IncidenciaListView.as_view(), name='lista_incidencias'),
    path('nueva/', IncidenciaCreateView.as_view(), name='crear_incidencia'),
]
