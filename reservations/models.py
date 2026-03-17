from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Appointment(models.Model):
    """Customer appointment in a fixed hourly schedule."""

    SERVICE_CHOICES = [
        ('consulta', 'Consulta'),
        ('servicio', 'Servicio'),
    ]

    PHONE_LENGTH = 10

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=PHONE_LENGTH)
    date = models.DateField()
    time = models.TimeField(default='00:00:00')
    service = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('date', 'time')
        constraints = [
            models.UniqueConstraint(fields=('date', 'time'), name='unique_appointment_slot'),
        ]

    def clean(self):
        """Keep validation rules in one place for forms and API usage."""
        super().clean()

        if len(self.phone) != self.PHONE_LENGTH or not self.phone.isdigit():
            raise ValidationError({'phone': 'El número de teléfono debe tener exactamente 10 dígitos.'})

        conflicting_appointment = Appointment.objects.filter(date=self.date, time=self.time).exclude(pk=self.pk)
        if conflicting_appointment.exists():
            raise ValidationError({'time': 'Ya existe una cita programada en esta fecha y hora.'})

    def __str__(self):
        return f'{self.name} - {self.service} ({self.date} {self.time})'
