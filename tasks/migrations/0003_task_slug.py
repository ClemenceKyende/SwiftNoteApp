# Generated by Django 5.1.3 on 2024-12-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_task_linked_note_task_linked_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
