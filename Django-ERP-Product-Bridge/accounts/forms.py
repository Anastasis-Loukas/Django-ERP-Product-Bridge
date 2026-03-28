from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Custom registration form extending Django's built-in UserCreationForm
class CustomUserCreationForm(UserCreationForm):

    # Override username field to customize label and styling
    username = forms.CharField(
        label="Όνομα Χρήστη",
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg"  # Bootstrap styling
        })
    )

    # Override password1 field (primary password input)
    password1 = forms.CharField(
        label="Κωδικός Πρόσβασης",
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg"
        })
    )

    # Override password2 field (password confirmation input)
    password2 = forms.CharField(
        label="Επιβεβαίωση Κωδικού",
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg"
        })
    )

    # Meta configuration linking the form to Django's User model
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    # Post-initialization customization
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove default Django help texts (e.g. password validation hints)
        for field in self.fields.values():
            field.help_text = None