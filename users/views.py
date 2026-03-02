from datetime import date, timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import redirect, render

from reservations.models import Appointment
from .forms import CustomUserCreationForm


def register(request):
    phone = request.GET.get('phone', '')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm(initial={'phone': phone})

    return render(request, 'users/register.html', {'form': form})


@login_required
def panel_home(request):
    if request.user.is_nutritionist:
        return redirect('admin_dashboard')
    return redirect('dashboard')


@login_required
def dashboard(request):
    if request.user.is_nutritionist:
        return redirect('admin_dashboard')

    appointments = Appointment.objects.filter(user=request.user).order_by('date', 'time')
    return render(request, 'users/dashboard.html', {'appointments': appointments})


@user_passes_test(lambda user: user.is_nutritionist, login_url='home')
def admin_dashboard(request):
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
        upcoming_appointments.values('name', 'phone').annotate(total_visits=Count('id')).order_by('-total_visits', 'name')[:5]
    )

    return render(
        request,
        'users/admin_dashboard.html',
        {
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
