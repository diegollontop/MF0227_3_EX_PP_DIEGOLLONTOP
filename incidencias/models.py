from django.db import models


class Tecnico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.especialidad})"


class Incidencia(models.Model):
    ESTADOS = [
        ('Abierto', 'Abierto'),
        ('En Proceso', 'En Proceso'),
        ('Cerrado', 'Cerrado'),
    ]

    PRIORIDADES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
        ('Critica', 'Crítica'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Abierto')
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='Media')
    tecnico = models.ForeignKey(
        Tecnico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidencias'
    )

    def __str__(self):
        return f"[{self.estado}] {self.titulo}"
