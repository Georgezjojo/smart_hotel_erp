import runpy
from pathlib import Path
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seeds the database with demo data (runs scripts/seed_data.py)'

    def handle(self, *args, **options):
        seed_script = Path('scripts/seed_data.py')
        if seed_script.exists():
            # Run the script with its own module globals so imports work correctly
            runpy.run_path(str(seed_script), run_name='__main__')
            self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        else:
            self.stderr.write(self.style.ERROR('scripts/seed_data.py not found'))