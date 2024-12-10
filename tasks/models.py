from django.db import models
from django.conf import settings
from notes.models import Note
from django.utils import timezone
import uuid
from django.utils.text import slugify
from django.core.mail import send_mail




class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    linked_notes = models.ManyToManyField(Note, blank=True, related_name='tasks')
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    slug = models.SlugField(unique=True, blank=True, null=True)

    # Fields for reminders and notifications
    reminder_time = models.DateTimeField(null=True, blank=True)  # Optional reminder time
    notification_sent = models.BooleanField(default=False)  # Track if notification is sent

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Task.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.title + str(uuid.uuid4()))  # Ensure uniqueness
        super().save(*args, **kwargs)

    def set_reminder(self):
        """Send email and in-app notifications if the reminder time is reached."""
        if self.reminder_time and timezone.now() >= self.reminder_time and not self.notification_sent:
            # Send email notification
            self.send_email_notification()
            # Create in-app notification
            self.create_in_app_notification()
            # Mark as notification sent
            self.notification_sent = True
            self.save()

    def send_email_notification(self):
        """Send an email reminder to the user."""
        send_mail(
            subject=f"Reminder: {self.title} is due!",
            message=f"Hello {self.user.username},\n\nYour task '{self.title}' is due soon. Please check your tasks.\n\nThanks, SwiftNote Team",
            from_email="noreply@swiftnote.com",
            recipient_list=[self.user.email],
        )

    def create_in_app_notification(self):
        """Log an in-app notification for the user."""
        Notification.objects.create(
            user=self.user,
            message=f"Reminder: Your task '{self.title}' is due soon.",
        )

    def __str__(self):
        return f"{self.title} - {self.status}" if len(self.title) <= 50 else self.title[:50] + "..."

    class Meta:
        unique_together = ('user', 'title')
        indexes = [
            models.Index(fields=['due_date']),
            models.Index(fields=['priority']),
        ]


class Notification(models.Model):
    """Model to store in-app notifications."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.created_at}"



