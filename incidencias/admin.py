from django.contrib import admin
from .models import Tecnico, Incidencia


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad', 'email')
    search_fields = ('nombre', 'especialidad')


@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado', 'prioridad', 'tecnico', 'fecha_creacion')
    list_filter = ('estado', 'prioridad')
    search_fields = ('titulo', 'tecnico__nombre')
