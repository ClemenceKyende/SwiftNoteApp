from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task

@shared_task
def send_task_reminder():
    """
    Sends reminders for tasks that are due soon and still pending.
    """
    tasks = Task.objects.filter(due_date__lte=timezone.now(), status='Pending')
    for task in tasks:
        if task.user and task.user.email:  # Ensure user and email exist
            send_mail(
                'Reminder: Your task is due soon!',
                f'The task "{task.title}" is due soon. Please check your tasks.',
                'from@example.com',  # Replace with your sender's email address
                [task.user.email],
            )
    return f"{tasks.count()} reminders sent."

@shared_task
def test_task():
    """
    A simple test task to verify Celery setup.
    """
    print("Celery task is working!")
    return "Task completed!"

@shared_task
def send_task_notifications():
    tasks = Task.objects.filter(reminder_time__lte=timezone.now(), notification_sent=False)
    for task in tasks:
        if task.user:
            message = f"Reminder: The task '{task.title}' is due soon."
            # Save notification to the database
            Notification.objects.create(
                user=task.user,
                message=message,
                task=task
            )
            # Optionally, you can also update task's notification_sent status
            task.notification_sent = True
            task.save()

    return f"{len(tasks)} task notifications sent."
