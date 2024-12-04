from django.urls import path
from . import views

urlpatterns = [
    # Task management URLs
    path('tasks/', views.view_tasks_view, name='view_tasks'),
    path('tasks/create/', views.create_task_view, name='create_task'),
    path('tasks/update/<int:task_id>/', views.update_task_view, name='update_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail'),
]
