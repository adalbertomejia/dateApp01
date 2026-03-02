from datetime import date, time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from reservations.models import Appointment
from users.forms import CustomUserCreationForm


class PanelHomeViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.admin_user = self.user_model.objects.create_user(
            username='admin',
            password='safe-pass-123',
            is_nutritionist=True,
            is_staff=True,
            is_superuser=True,
        )
        self.patient_user = self.user_model.objects.create_user(
            username='paciente',
            password='safe-pass-123',
            is_nutritionist=False,
            is_patient=True,
        )

    def test_nutritionist_redirected_to_admin_panel(self):
        self.client.login(username='admin', password='safe-pass-123')

        response = self.client.get(reverse('panel_home'))

        self.assertRedirects(response, '/admin/')

    def test_patient_redirected_to_home(self):
        self.client.login(username='paciente', password='safe-pass-123')

        response = self.client.get(reverse('panel_home'))

        self.assertRedirects(response, reverse('home'))


class AdminIndexViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.admin_user = self.user_model.objects.create_user(
            username='admin',
            password='safe-pass-123',
            is_nutritionist=True,
            is_staff=True,
            is_superuser=True,
        )
        self.patient_user = self.user_model.objects.create_user(
            username='paciente',
            password='safe-pass-123',
            is_nutritionist=False,
            is_patient=True,
            is_staff=True,
        )

    def test_nutritionist_sees_custom_admin_dashboard(self):
        Appointment.objects.create(
            name='Client One',
            phone='5511111111',
            date=date.today(),
            time=time(9, 0),
            service='consulta',
        )

        self.client.login(username='admin', password='safe-pass-123')
        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Panel de administración')
        self.assertContains(response, 'Client One')

    def test_non_nutritionist_cannot_access_custom_admin_dashboard(self):
        self.client.login(username='paciente', password='safe-pass-123')
        response = self.client.get('/admin/')

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
