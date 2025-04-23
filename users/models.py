from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=True)
    is_nutritionist = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True, null=True)