from collections import defaultdict
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render

from .models import Appointment


BUSINESS_CONTEXT = {
    'business_name': 'Nutriologa María Pérez',
    'business_address': 'Calle Salud #123, Ciudad',
    'business_description': 'Especialista en nutrición y bienestar.',
}

WORKING_HOURS = ['09:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00']


def home(request):
    return render(request, 'reservations/home.html', BUSINESS_CONTEXT)


def _build_schedule(start_date, days=7):
    end_date = start_date + timedelta(days=days - 1)
    appointments = (
        Appointment.objects.filter(date__range=(start_date, end_date))
        .values_list('date', 'time')
        .order_by('date', 'time')
    )

    occupied_by_day = defaultdict(set)
    for appointment_date, appointment_time in appointments:
        occupied_by_day[appointment_date].add(appointment_time.strftime('%H:%M:%S'))

    schedule = {}
    for day in (start_date + timedelta(days=i) for i in range(days)):
        occupied_hours = occupied_by_day.get(day, set())
        schedule[day] = [
            {'hour': hour, 'status': 'Ocupada' if hour in occupied_hours else 'Disponible'}
            for hour in WORKING_HOURS
        ]

    return schedule, end_date


def book_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        appointment_date = request.POST.get('date')
        time = request.POST.get('time')
        service = request.POST.get('service')
        note = request.POST.get('note', '')

        appointment = Appointment(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            phone=phone,
            date=appointment_date,
            time=time,
            service=service,
            note=note,
        )

        try:
            appointment.full_clean()
            appointment.save()
            return render(
                request,
                'reservations/confirmation.html',
                {
                    'name': name,
                    'service': service,
                    'date': appointment_date,
                    'time': time,
                    'phone': phone,
                },
            )
        except ValidationError:
            today = date.today()
            schedule, end_date = _build_schedule(today)
            context = {
                'schedule': schedule,
                'start_date': today,
                'end_date': end_date,
                'error_message': 'La fecha y hora seleccionadas ya están ocupadas. Por favor, elige otra.',
            }
            return render(request, 'reservations/available_appointments.html', context)

    return render(request, 'reservations/home.html', BUSINESS_CONTEXT)


def get_unavailable_slots(request):
    appointments = Appointment.objects.values('date', 'time')
    unavailable_slots = list(appointments)
    return JsonResponse(unavailable_slots, safe=False)


def available_appointments(request):
    today = date.today()
    schedule, end_date = _build_schedule(today)
    return render(
        request,
        'reservations/available_appointments.html',
        {
            'schedule': schedule,
            'start_date': today,
            'end_date': end_date,
        },
    )
