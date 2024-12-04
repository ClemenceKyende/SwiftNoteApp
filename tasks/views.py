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
        form = TaskForm(request.POST, user=request.user, instance=task)  # Pass the logged-in user to the form
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Ensure the task is assigned to the logged-in user
            task.save()  # Save the task to the database

            # Handle the many-to-many relationship with notes
            linked_notes = form.cleaned_data['linked_notes']
            task.linked_notes.set(linked_notes)  # Assign selected notes to the task

            # Success message with a link to view tasks
            success_message = format_html(
                'Task updated successfully!</a>',
                reverse("view_tasks")
            )
            messages.success(request, success_message)
            return redirect('view_tasks')  # Redirect to the view tasks page after update

    else:
        form = TaskForm(user=request.user, instance=task)  # Pass the logged-in user to the form

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

