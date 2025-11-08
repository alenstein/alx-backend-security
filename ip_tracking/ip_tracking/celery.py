import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the celery program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ip_tracking.settings')

app = Celery('ip_tracking')

# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Define the periodic task (beat schedule)
app.conf.beat_schedule = {
    'detect-suspicious-ips-hourly': {
        'task': 'ip_tracking.tasks.detect_suspicious_ips',
        'schedule': crontab(minute='0', hour='*'),  # Runs at the start of every hour
    },
}