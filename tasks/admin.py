from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'user', 'due_date')
    search_fields = ('title', 'user__username', 'linked_notes__title')
    ordering = ('-created_at',)
    filter_horizontal = ('linked_notes',)

    # Group fields into sections for the form (more control)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'status', 'priority', 'due_date')
        }),
        ('Linked Notes', {
            'fields': ('linked_notes',)
        }),
        ('Meta Information', {
            'fields': ('user', 'created_at', 'updated_at'),
            'classes': ('collapse',)  # This hides the section by default
        }),
    )

admin.site.register(Task, TaskAdmin)