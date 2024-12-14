from django.urls import path
from . import views
from .views import NotificationListView
from .views import mark_as_read


urlpatterns = [
    # Task management URLs
    path('tasks/', views.view_tasks_view, name='view_tasks'),
    path('tasks/create/', views.create_task_view, name='create_task'),
    path('tasks/update/<int:task_id>/', views.update_task_view, name='update_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', mark_as_read, name='mark_as_read'), path('trigger-reminder/', views.trigger_reminder, name='trigger_reminder'),
]

