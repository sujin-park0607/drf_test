from django.core.management.base import BaseCommand
from django_seed import Seed
from api.models import Stay
from faker import Faker

class Command(BaseCommand):
    def handle(self, *args, **options):
        f = Faker()
        seeder = Seed.seeder()

        for _ in range(1000):
            seeder.add_entity(Stay, 1,
                {
                    "place": "Seongan-gil",
                    "dateTime": f.date_time_between('-3years','now'),
                    "inout": 1,
                }
            )
        seeder.execute()
    