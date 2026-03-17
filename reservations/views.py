from collections import defaultdict
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render

from users.models import CustomUser

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
    """Create availability map for the next N days."""
    end_date = start_date + timedelta(days=days - 1)
    appointments = (
        Appointment.objects.filter(date__range=(start_date, end_date))
        .values_list('date', 'time')
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


def _availability_context(error_message=None):
    """Shared context for the weekly availability page."""
    today = date.today()
    schedule, end_date = _build_schedule(today)
    context = {
        'schedule': schedule,
        'start_date': today,
        'end_date': end_date,
    }
    if error_message:
        context['error_message'] = error_message
    return context


def _first_validation_message(error):
    """Return a human-friendly first validation error message."""
    if hasattr(error, 'message_dict') and error.message_dict:
        first_field_errors = next(iter(error.message_dict.values()))
        if first_field_errors:
            return first_field_errors[0]

    if getattr(error, 'messages', None):
        return error.messages[0]

    return 'No fue posible registrar la cita. Verifica los datos e inténtalo de nuevo.'


def book_appointment(request):
    if request.method != 'POST':
        return render(request, 'reservations/home.html', BUSINESS_CONTEXT)

    appointment_data = {
        'name': request.POST.get('name'),
        'phone': request.POST.get('phone'),
        'date': request.POST.get('date'),
        'time': request.POST.get('time'),
        'service': request.POST.get('service'),
        'note': request.POST.get('note', ''),
    }

    related_user = (
        request.user
        if request.user.is_authenticated
        else CustomUser.objects.filter(phone=appointment_data['phone']).first()
    )

    appointment = Appointment(user=related_user, **appointment_data)

    try:
        appointment.full_clean()
        appointment.save()
    except ValidationError as error:
        context = _availability_context(_first_validation_message(error))
        return render(request, 'reservations/available_appointments.html', context)

    return render(
        request,
        'reservations/confirmation.html',
        {
            **appointment_data,
            'related_user': related_user,
        },
    )


def get_unavailable_slots(request):
    appointments = Appointment.objects.values('date', 'time')
    return JsonResponse(list(appointments), safe=False)


def available_appointments(request):
    return render(
        request,
        'reservations/available_appointments.html',
        _availability_context(),
    )
