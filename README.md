# Smart Hotel ERP

Complete hotel management, reservation, POS, and BI platform.

## Setup
1. Create virtual environment and install dependencies.
2. Set up MySQL database and update .env.
3. Run migrations: python manage.py migrate
4. Seed data: python manage.py shell < scripts/seed_data.py
5. Start server: python manage.py runserver