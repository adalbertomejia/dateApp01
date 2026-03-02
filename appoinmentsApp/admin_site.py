from datetime import date, timedelta

from django.contrib.admin import AdminSite
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.utils.decorators import method_decorator

from reservations.models import Appointment


class NutritionAdminSite(AdminSite):
    site_header = 'Panel de nutrición'
    site_title = 'Panel admin'
    index_title = 'Resumen administrativo'

    @method_decorator(user_passes_test(lambda user: user.is_nutritionist, login_url='home', redirect_field_name=REDIRECT_FIELD_NAME))
    def index(self, request, extra_context=None):
        today = date.today()
        week_end = today + timedelta(days=6)

        all_appointments = Appointment.objects.order_by('date', 'time')
        today_appointments = all_appointments.filter(date=today)
        upcoming_appointments = all_appointments.filter(date__gte=today)

        occupancy_rate = int((today_appointments.count() / 7) * 100) if today_appointments.exists() else 0

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

        context = {
            'today_appointments': today_appointments,
            'upcoming_appointments': upcoming_appointments[:12],
            'appointments_by_service': appointments_by_service,
            'recent_clients': recent_clients,
            'total_appointments': all_appointments.count(),
            'today_total': today_appointments.count(),
            'upcoming_total': upcoming_appointments.count(),
            'occupancy_rate': occupancy_rate,
            **(extra_context or {}),
        }
        return super().index(request, extra_context=context)


nutrition_admin_site = NutritionAdminSite(name='nutrition_admin')
