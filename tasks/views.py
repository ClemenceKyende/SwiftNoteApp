from django.db import IntegrityError  # Import the IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.utils.html import format_html
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Notification
from django.utils import timezone
from datetime import datetime


@login_required
def create_task_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                task = form.save(commit=False)
                task.user = request.user
                task.slug = slugify(task.title)
                task.save()

                # Handle many-to-many notes relationship
                linked_notes = form.cleaned_data['linked_notes']
                task.linked_notes.set(linked_notes)

                success_message = format_html(
                    'Task created successfully! <a href="{}" class="btn btn-link">Click here to view your tasks</a>',
                    reverse("view_tasks")
                )
                messages.success(request, success_message)
                return redirect('create_task')
            except IntegrityError:
                messages.error(request, "Invalid form submission. Please check your input.")
        else:
            messages.error(request, "A task with this title already exists. Please choose a different title.")
    else:
        form = TaskForm(user=request.user)

    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def update_task_view(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        raise Http404("Task not found")

    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            # Handle the many-to-many relationship with notes
            linked_notes = form.cleaned_data['linked_notes']
            task.linked_notes.set(linked_notes)

            # Success message
            success_message = "Task updated successfully!"
            messages.success(request, success_message)
            return redirect('view_tasks')
    else:
        form = TaskForm(user=request.user, instance=task)

    return render(request, 'tasks/update_task.html', {'form': form, 'task': task})


# View for deleting a task
@login_required
def delete_task_view(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        raise Http404("Task not found")

    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return HttpResponseRedirect(reverse("view_tasks"))  # Redirect after deleting the task

    return render(request, "tasks/delete_task.html", {"task": task})

@login_required
def view_tasks_view(request):
    search_query = request.GET.get('search', '').strip()
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    no_results = False

    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))  # Adjust this based on your model
        if not tasks.exists():
            no_results = True

    paginator = Paginator(tasks, 5)  # Adjust the number of tasks per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "tasks/view_tasks.html", {
        "page_obj": page_obj,
        "search_query": search_query,
        "no_results": no_results,
    })

@login_required
def task_detail_view(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)  # Fetch the task by ID and ensure it's owned by the logged-in user
    return render(request, "tasks/task_detail.html", {"task": task})


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications.html', {'notifications': notifications})

class NotificationListView(ListView):
    model = Notification
    template_name = 'tasks/notifications.html'
    context_object_name = 'notifications'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to login page if the user is not authenticated
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter notifications for the logged-in user
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

# Mark a notification as read
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')  # Assuming 'notifications' is the URL name for the list of notifications


