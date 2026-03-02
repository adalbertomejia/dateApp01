from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from reservations.models import Appointment
from .forms import CustomUserCreationForm

def register(request):
    phone = request.GET.get('phone', '')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # o a donde quieras
    else:
        form = CustomUserCreationForm(initial={'phone': phone})

    return render(request, 'users/register.html', {'form': form})


@login_required
def dashboard(request):
    appointments = (
        Appointment.objects.filter(user=request.user)
        .order_by('date', 'time')
    )
    return render(
        request,
        'users/dashboard.html',
        {'appointments': appointments},
    )
