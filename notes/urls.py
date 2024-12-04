from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
    path('register/', views.register_view, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout
    path('create-note/', views.create_note_view, name='create_note'),  # Create Note page
    path('view-notes/', views.view_notes_view, name='view_notes'), # View Notes page
    path('update-note/<int:note_id>/', views.update_note_view, name='update_note'),
    path('delete-note/<int:note_id>/', views.delete_note_view, name='delete_note'),
    path('note/<int:note_id>/', views.note_detail_view, name='note_detail'),
]