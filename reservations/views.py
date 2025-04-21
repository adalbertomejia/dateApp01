# filepath: /home/Adal/Python projects/reservations/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Appointment

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