FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install only what's needed for psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Provide a dummy database so collectstatic can run (SQLite – always available)
ENV DATABASE_URL=sqlite:///dummy.db

# Now collect static files without trying to connect to MySQL
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Start Daphne (ASGI) on the port Railway provides
CMD ["sh", "-c", "daphne -b 0.0.0.0 -p $PORT config.asgi:application"]