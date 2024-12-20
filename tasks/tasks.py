from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task, Notification
from django.core.mail import send_mail  # or another method for notifications

@shared_task
def send_notification(user_email, message):
    # This is just an example of sending an email notification.
    send_mail(
        'Reminder from SwiftNote',
        message,
        'no-reply@swiftnote.com',  # Use your project's email address
        [user_email],
        fail_silently=False,
    )


@shared_task
def send_task_reminder():
    tasks = Task.objects.filter(due_date__lte=timezone.now(), status='Pending')
    reminders_sent = 0
    for task in tasks:
        print(f"Processing task: {task.id} - {task.title}")  # Add more logging for better insights
        if task.user and task.user.email:
            try:
                send_mail(
                    'Reminder: Your task is due soon!',
                    f'The task "{task.title}" is due soon. Please check your tasks.',
                    'mwendeclemence@mail.com',
                    [task.user.email],
                )
                reminders_sent += 1
            except Exception as e:
                print(f"Failed to send email for task {task.id}: {e}")
    return f"{reminders_sent} reminders sent."

@shared_task
def send_task_notifications():
    """
    Sends in-app notifications for tasks that are due soon.
    """
    tasks = Task.objects.filter(reminder_time__lte=timezone.now(), notification_sent=False)
    notifications_sent = 0
    for task in tasks:
        if task.user:
            try:
                # Save notification to the database
                Notification.objects.create(
                    user=task.user,
                    message=f"Reminder: The task '{task.title}' is due soon.",
                    task=task
                )
                # Update task's notification_sent status
                task.notification_sent = True
                task.save()
                notifications_sent += 1
            except Exception as e:
                print(f"Failed to create notification for task {task.id}: {e}")
    return f"{notifications_sent} task notifications sent."


@shared_task
def test_task():
    """
    A simple test task to verify Celery setup.
    """
    print("Celery task is working!")
    return "Task completed!"


@shared_task
def example_task():
    """
    Another example task.
    """
    print("Task executed!")
    return "Task executed successfully!"


@shared_task
def check_and_send_reminders():
    """Checks all tasks and sends reminders if needed."""
    tasks = Task.objects.filter(reminder_time__lte=timezone.now(), notification_sent=False)
    reminders_sent = 0
    for task in tasks:
        try:
            task.set_reminder()  # Update the reminder if needed
            if task.user and task.user.email:  # Ensure user and email exist
                send_mail(
                    'Reminder: Your task is due soon!',
                    f'The task "{task.title}" is due soon. Please check your tasks.',
                    'from@example.com',  # Replace with your sender's email address
                    [task.user.email],
                )
                reminders_sent += 1
                task.notification_sent = True
                task.save()  # Mark task as notified
        except Exception as e:
            print(f"Failed to send reminder for task {task.id}: {e}")
    return f"{reminders_sent} reminders sent."

@shared_task
def add(x, y):
    return x + y