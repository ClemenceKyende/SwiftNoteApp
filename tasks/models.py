from django.db import models
from django.conf import settings
from notes.models import Note


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
    slug = models.SlugField(unique=True, blank=True, null=True)  # New slug field

    def save(self, *args, **kwargs):
        # Automatically generate the slug if it is not set
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure the slug is unique
            while Task.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.title + str(uuid.uuid4()))  # Add a UUID to make the slug unique
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('user', 'title')
        indexes = [
            models.Index(fields=['due_date']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f"{self.title} - {self.status}" if len(self.title) <= 50 else self.title[:50] + "..."
