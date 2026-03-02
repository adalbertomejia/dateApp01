from datetime import date, time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from reservations.models import Appointment


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='maria',
            password='safe-pass-123',
        )
        self.other_user = self.user_model.objects.create_user(
            username='otro',
            password='safe-pass-123',
        )

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_dashboard_shows_only_logged_user_appointments(self):
        Appointment.objects.create(
            user=self.user,
            name='Maria User',
            phone='5512345678',
            date=date(2026, 1, 10),
            time=time(9, 0),
            service='consulta',
        )
        Appointment.objects.create(
            user=self.other_user,
            name='Other User',
            phone='5598765432',
            date=date(2026, 1, 11),
            time=time(10, 0),
            service='servicio',
        )

        self.client.login(username='maria', password='safe-pass-123')
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria User')
        self.assertNotContains(response, 'Other User')
