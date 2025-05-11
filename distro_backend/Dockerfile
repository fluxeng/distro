FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files during build
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "config.wsgi:application"]