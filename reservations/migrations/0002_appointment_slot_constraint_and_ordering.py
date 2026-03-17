from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(fields=('date', 'time'), name='unique_appointment_slot'),
        ),
    ]
