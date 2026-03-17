from datetime import date, time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from reservations.models import Appointment


class BookingFlowTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='maria',
            password='safe-pass-123',
            phone='5512345678',
        )

    def test_booking_links_existing_user_by_phone(self):
        response = self.client.post(
            reverse('book_appointment'),
            {
                'name': 'Paciente Uno',
                'phone': '5512345678',
                'date': date(2026, 1, 10).isoformat(),
                'time': '09:00',
                'service': 'consulta',
                'note': 'Primera visita',
            },
        )

        appointment = Appointment.objects.get(phone='5512345678')
        self.assertEqual(appointment.user, self.user)
        self.assertContains(response, 'Detectamos una cuenta existente con este teléfono')


    def test_booking_shows_model_validation_message_for_invalid_phone(self):
        response = self.client.post(
            reverse('book_appointment'),
            {
                'name': 'Paciente Inválido',
                'phone': '55ABC45678',
                'date': date(2026, 1, 12).isoformat(),
                'time': '11:00',
                'service': 'consulta',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'exactamente 10 dígitos')

    def test_home_shows_logout_button_for_authenticated_user(self):
        self.client.login(username='maria', password='safe-pass-123')

        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Cerrar sesión')


class AppointmentModelTests(TestCase):
    def test_rejects_phone_with_non_numeric_characters(self):
        appointment = Appointment(
            name='Paciente Dos',
            phone='55ABC45678',
            date=date(2026, 1, 10),
            time=time(9, 0),
            service='consulta',
        )

        with self.assertRaises(ValidationError):
            appointment.full_clean()

    def test_allows_updating_existing_appointment_without_false_duplicate(self):
        appointment = Appointment.objects.create(
            name='Paciente Tres',
            phone='5512345678',
            date=date(2026, 1, 10),
            time=time(10, 0),
            service='consulta',
        )
        appointment.note = 'Actualización de nota'

        appointment.full_clean()
        appointment.save()

        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(Appointment.objects.first().note, 'Actualización de nota')
