from django.contrib import admin
from .models import CustomUser, Note
from django.conf import settings

# Register the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']  # Fields to display in the admin

# Register the Note model
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']  # Fields to display in the admin
