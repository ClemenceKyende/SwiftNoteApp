import os
from celery import Celery
from celery.schedules import crontab  # Import crontab for periodic tasks
import json

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiftnote.settings')

# Create an instance of the Celery app
app = Celery('tasks', broker='redis://localhost:6379/0')  # Redis as broker

# Celery configurations)

# Use the settings from Django, prefixing them with 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configure serializers
app.conf.task_serializer = 'pickle'
app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.accept_content = ['pickle']  # Allow only JSON content
app.conf.result_serializer = 'pickle'
app.conf.timezone = 'UTC'

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Define the periodic tasks (using Celery Beat)
app.conf.beat_schedule = {
    'send-task-reminders': {
        'task': 'swiftnote.tasks.send_task_reminder',
        'schedule': crontab(minute='*/1'),  # Run every minute (adjust for production)
    },
    'send-task-notifications': {
        'task': 'swiftnote.tasks.send_task_notifications',
        'schedule': crontab(minute='*/5'),  # Example: every 5 minutes (adjust as needed)
    },
    'check-send-reminders': {
        'task': 'swiftnote.tasks.check_and_send_reminders',
        'schedule': crontab(minute='*/10'),  # Every 10 minutes, for example
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
