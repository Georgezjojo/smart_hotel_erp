from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seeds the database with demo data (runs scripts/seed_data.py)'

    def handle(self, *args, **options):
        # Execute the seed script
        exec(open('scripts/seed_data.py').read())
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))