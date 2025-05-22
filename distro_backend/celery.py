# distro_backend/celery.py
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distro_backend.settings')

app = Celery('distro_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Africa/Nairobi',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Periodic tasks (you can add these later)
app.conf.beat_schedule = {
    'send-daily-reports': {
        'task': 'utilities.tasks.send_daily_reports',
        'schedule': 86400.0,  # Every 24 hours
    },
    'check-critical-assets': {
        'task': 'infrastructure.tasks.check_critical_assets',
        'schedule': 3600.0,  # Every hour
    },
}


# distro_backend/__init__.py
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)