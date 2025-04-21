from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('consulta', 'Consulta'),
        ('servicio', 'Servicio'),
    ]

    name = models.CharField(max_length=100)  # Nombre del cliente
    phone = models.CharField(max_length=10)  # Nuevo campo para el teléfono
    date = models.DateField()  # Fecha de la cita
    time = models.TimeField(default="00:00:00")  # Nuevo campo para el horario
    service = models.CharField(max_length=10, choices=SERVICE_CHOICES)  # Tipo de servicio
    note = models.TextField(blank=True, null=True)  # Nota opcional

    def clean(self):
        # Validación de longitud del número de teléfono
        if len(self.phone) != 10:
            raise ValidationError("El número de teléfono debe tener exactamente 10 caracteres.")

        # Validación para evitar citas duplicadas
        if Appointment.objects.filter(date=self.date, time=self.time).exists():
            raise ValidationError("Ya existe una cita programada en esta fecha y hora.")

    def __str__(self):
        return f"{self.name} - {self.service} ({self.date} {self.time})"