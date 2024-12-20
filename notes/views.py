from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.html import format_html
from .forms import CustomUserRegistrationForm
from .models import Note
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404



# Home view to display the user's note count
@login_required
def home_view(request):
    notes_count = Note.objects.filter(user=request.user).count()
    return render(request, "notes/home.html", {
        "notes_count": notes_count
    })

@login_required
def create_note_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            messages.error(request, "Both title and content are required.")
        else:
            try:
                # Try to create the note
                note = Note.objects.create(user=request.user, title=title, content=content)
                success_message = format_html(
                    'Note created successfully! <a href="{}" class="btn btn-link">Click here to view your notes</a>',
                    reverse("view_notes")
                )
                messages.success(request, success_message)
                return redirect("create_note")

            except IntegrityError:
                # Handle the case where the note already exists due to a unique constraint (e.g., slug)
                messages.error(request, "A note with this title already exists. Please choose a different title.")

    return render(request, "notes/create_note.html")
# View for updating an existing note
@login_required
def update_note_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        raise Http404("Note not found")

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            messages.error(request, "Both title and content are required.")
        else:
            note.title = title
            note.content = content
            note.save()
            messages.success(request, "Note updated successfully!")
            return redirect("view_notes")

    return render(request, "notes/update_note.html", {"note": note})


# View for deleting an existing note
@login_required
def delete_note_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        raise Http404("Note not found")

    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted successfully!")
        return redirect("view_notes")

    return render(request, "notes/delete_note.html", {"note": note})


# View for displaying all notes
@login_required
def view_notes_view(request):
    search_query = request.GET.get('search', '').strip()
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    no_results = False

    if search_query:
        notes = notes.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
        if not notes.exists():
            no_results = True

    paginator = Paginator(notes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "notes/view_notes.html", {
        "page_obj": page_obj,
        "search_query": search_query,
        "no_results": no_results,
    })

# Registration view for creating new users
def register_view(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Registration failed. Please check the form for errors.")
    else:
        form = CustomUserRegistrationForm()

    return render(request, "notes/register.html", {"form": form})


# Login view for existing users
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "notes/login.html")


# Logout view for users
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return HttpResponseRedirect("/")

# views.py
def note_detail_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})
