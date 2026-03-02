from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
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
    if request.user.is_nutritionist:
        today = date.today()
        week_end = today + timedelta(days=6)

        all_appointments = Appointment.objects.order_by('date', 'time')
        today_appointments = all_appointments.filter(date=today)
        upcoming_appointments = all_appointments.filter(date__gte=today)

        occupancy_rate = int((today_appointments.count() / 7) * 100) if today_appointments else 0

        appointments_by_service = list(
            upcoming_appointments
            .filter(date__range=(today, week_end))
            .values('service')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        service_labels = dict(Appointment.SERVICE_CHOICES)
        for item in appointments_by_service:
            item['label'] = service_labels.get(item['service'], item['service'])

        recent_clients = (
            upcoming_appointments
            .values('name', 'phone')
            .annotate(total_visits=Count('id'))
            .order_by('-total_visits', 'name')[:5]
        )

        return render(
            request,
            'users/dashboard.html',
            {
                'is_admin_panel': True,
                'today_appointments': today_appointments,
                'upcoming_appointments': upcoming_appointments[:12],
                'appointments_by_service': appointments_by_service,
                'recent_clients': recent_clients,
                'total_appointments': all_appointments.count(),
                'today_total': today_appointments.count(),
                'upcoming_total': upcoming_appointments.count(),
                'occupancy_rate': occupancy_rate,
            },
        )

    appointments = (
        Appointment.objects.filter(user=request.user)
        .order_by('date', 'time')
    )
    return render(
        request,
        'users/dashboard.html',
        {'appointments': appointments, 'is_admin_panel': False},
    )
