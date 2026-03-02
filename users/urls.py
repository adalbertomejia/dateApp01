from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('panel/', views.panel_home, name='panel_home'),
]
