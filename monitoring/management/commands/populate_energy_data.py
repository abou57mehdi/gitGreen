from django.core.management.base import BaseCommand
from monitoring.models import EnergyData
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample energy data'

    def handle(self, *args, **kwargs):
        EnergyData.objects.all().delete()  # Clear existing data
        for _ in range(100):  # Generate 100 sample records
            timestamp = datetime.now() - timedelta(minutes=5 * _)
            energy_consumption = random.uniform(50, 200)
            EnergyData.objects.create(timestamp=timestamp, energy_consumption=energy_consumption)
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data'))
