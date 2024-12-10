import os
from celery import Celery
from celery.schedules import crontab  # Import crontab for periodic tasks

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiftnote.settings')

# Create an instance of the Celery app
app = Celery('swiftnote')

# Use the settings from Django, prefixing them with 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Define the periodic tasks (using Celery Beat)
app.conf.beat_schedule = {
    'send-task-reminders': {
        'task': 'swiftnote.tasks.send_task_reminder',  # Fully qualified task name
        'schedule': crontab(minute='*/1'),  # Run every minute (adjust for production)
    },
    'send-task-notifications': {
        'task': 'swiftnote.tasks.send_task_notifications',
        'schedule': crontab(minute='*/5'),  # Example: every 5 minutes (adjust as needed)
    },
}

@app.task(bind=True)
def debug_task(self):
    """A simple debug task to verify Celery is working."""
    print(f'Request: {self.request!r}')
