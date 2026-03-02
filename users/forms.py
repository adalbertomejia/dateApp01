from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone

        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Este teléfono ya está registrado. Inicia sesión con tu cuenta.')

        return phone
