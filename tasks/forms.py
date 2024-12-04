from django import forms
from notes.models import Note
from .models import Task

class TaskForm(forms.ModelForm):
    linked_notes = forms.ModelMultipleChoiceField(
        queryset=Note.objects.none(),  # Default to an empty queryset
        required=False,
        widget=forms.SelectMultiple,  # Multi-select dropdown
        label="Linked Notes"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'linked_notes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            # Filter notes based on the user
            self.fields['linked_notes'].queryset = Note.objects.filter(user=user)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Check if a task with the same title already exists
        if Task.objects.filter(title=title).exists():
            raise forms.ValidationError('A task with this title already exists.')
        return title