from datetime import date, time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from reservations.models import Appointment
from users.forms import CustomUserCreationForm


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


class AdminDashboardViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.admin_user = self.user_model.objects.create_user(
            username='admin',
            password='safe-pass-123',
            is_nutritionist=True,
            is_patient=False,
        )
        self.patient_user = self.user_model.objects.create_user(
            username='paciente',
            password='safe-pass-123',
            is_nutritionist=False,
            is_patient=True,
        )

    def test_nutritionist_sees_admin_panel(self):
        Appointment.objects.create(
            name='Client One',
            phone='5511111111',
            date=date.today(),
            time=time(9, 0),
            service='consulta',
        )

        self.client.login(username='admin', password='safe-pass-123')
        response = self.client.get(reverse('admin_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Panel de administración')
        self.assertContains(response, 'Client One')

    def test_nutritionist_redirected_from_user_dashboard(self):
        self.client.login(username='admin', password='safe-pass-123')
        response = self.client.get(reverse('dashboard'))

        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_patient_cannot_access_admin_dashboard(self):
        self.client.login(username='paciente', password='safe-pass-123')
        response = self.client.get(reverse('admin_dashboard'))

        self.assertRedirects(response, reverse('home'))


class CustomUserCreationFormTests(TestCase):
    def test_rejects_repeated_phone(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username='existing',
            password='safe-pass-123',
            phone='5512345678',
        )

        form = CustomUserCreationForm(
            data={
                'username': 'nuevo',
                'email': 'nuevo@example.com',
                'phone': '5512345678',
                'password1': 'OtherSafePass123!',
                'password2': 'OtherSafePass123!',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('Este teléfono ya está registrado', form.errors['phone'][0])
