FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install only what's needed for psycopg2-binary (build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files into STATIC_ROOT
RUN python manage.py collectstatic --noinput

# Railway provides $PORT – bind with Daphne (ASGI)
CMD daphne -b 0.0.0.0 -p $PORT config.asgi:application