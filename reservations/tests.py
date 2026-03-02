from datetime import date

from django.contrib.auth import get_user_model
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

    def test_home_shows_logout_button_for_authenticated_user(self):
        self.client.login(username='maria', password='safe-pass-123')

        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Cerrar sesión')
