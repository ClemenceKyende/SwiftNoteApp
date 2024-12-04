from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),  # Notes app URLs
    path('', include('tasks.urls')),
]
