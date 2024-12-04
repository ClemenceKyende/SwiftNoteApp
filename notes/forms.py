from django import forms
from .models import CustomUser, Note


class CustomUserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a strong password'}),
        help_text="Enter a strong password.",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        help_text="Enter the same password as above for verification.",
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add form-control class to all fields
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter a unique username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter a valid email address'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Re-enter the password'})


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Generate the slug from the title
        slug = slugify(title)
        # Check if the slug already exists
        if Note.objects.filter(slug=slug).exists():
            raise forms.ValidationError('A note with this title already exists.')
        return title

    def save(self, commit=True):
        note = super().save(commit=False)
        # Automatically generate slug when saving the note
        note.slug = slugify(note.title)
        # Ensure the slug is unique
        while Note.objects.filter(slug=note.slug).exists():
            note.slug = slugify(note.title) + '-' + str(Note.objects.filter(slug=note.slug).count() + 1)

        if commit:
            note.save()
        return note