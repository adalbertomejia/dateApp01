# filepath: /home/Adal/Python projects/reservations/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Appointment
from datetime import date, timedelta  # Para manejar fechas y rangos de días

def home(request):
    context = {
        'business_name': 'Nutriologa María Pérez',
        'business_address': 'Calle Salud #123, Ciudad',
        'business_description': 'Especialista en nutrición y bienestar.',
    }
    return render(request, 'reservations/home.html', context)

def book_appointment(request):
    if request.method == 'POST':
        # Capturar los datos enviados por el formulario
        name = request.POST.get('name')
        phone = request.POST.get('phone')  # Cambiado de email a phone
        date = request.POST.get('date')
        time = request.POST.get('time')  # Captura el valor del campo 'time'
        service = request.POST.get('service')
        service = request.POST.get('service')
        note = request.POST.get('note', '')

        # Guardar los datos en la base de datos
        appointment = Appointment(
            name=name,
            phone=phone,
            date=date,
            time=time,
            service=service,
            note=note
        )
        appointment.full_clean()  # Esto ejecuta las validaciones definidas en el modelo
        appointment.save()  # Solo se ejecutará si no hay errores de validación
        # Redirigir a la página de confirmación
        return render(request, 'reservations/confirmation.html', {
            'name': name,
            'service': service,
            'date': date,
            'time': time,
        })
    
    return render(request, 'reservations/home.html')

def get_unavailable_slots(request):
    # Obtén todas las citas existentes
    appointments = Appointment.objects.values('date', 'time')

    # Convierte las citas en una lista de diccionarios
    unavailable_slots = list(appointments)

    # Devuelve los datos en formato JSON
    return JsonResponse(unavailable_slots, safe=False)

def available_appointments(request):
    """
    Muestra las citas disponibles y ocupadas en una tabla, de lunes a sábado.
    """
    # Obtén la fecha actual
    today = date.today()

    # Calcula las fechas de lunes a sábado (rango de 6 días)
    start_date = today
    end_date = today + timedelta(days=6)

    # Obtén todas las citas dentro del rango de fechas
    appointments = Appointment.objects.filter(date__range=(start_date, end_date)).order_by('date', 'time')

    # Define las horas laborales (de 9:00 AM a 3:00 PM)
    all_hours = ['09:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00']

    # Crear un diccionario para almacenar las horas disponibles y ocupadas por día
    schedule = {}

    # Iterar sobre cada día en el rango de lunes a sábado
    for day in (start_date + timedelta(days=i) for i in range(6)):
        # Obtener las horas ocupadas para el día actual
        occupied_hours = appointments.filter(date=day).values_list('time', flat=True)

        # Convertir las horas ocupadas al formato de cadenas 'HH:MM:SS'
        occupied_hours = [hour.strftime('%H:%M:%S') for hour in occupied_hours]

        # Crear una lista con el estado de cada hora (ocupada o disponible)
        schedule[day] = [
            {'hour': hour, 'status': 'Ocupada' if hour in occupied_hours else 'Disponible'}
            for hour in all_hours
        ]

    # Renderiza la tabla en el template
    return render(request, 'reservations/available_appointments.html', {
        'schedule': schedule,
        'start_date': start_date,
        'end_date': end_date
    })