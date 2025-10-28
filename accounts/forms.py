from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import User


class _FormControlMixin:
    """Apply Bootstrap classes to widgets automatically."""
    def _style(self):
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = (css + " form-check-input").strip()
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = (css + " form-select").strip()
            else:
                field.widget.attrs["class"] = (css + " form-control").strip()


class RegistrationForm(_FormControlMixin, UserCreationForm):
    # Only allow public registration for seekers and employers
    ROLE_CHOICES = [
        ("seeker", "Job Seeker"),
        ("employer", "Employer"),
    ]

    email = forms.EmailField(max_length=100, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name",
            "contact_number", "city", "role",
            "password1", "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Nice placeholders
        placeholders = {
            "username": "jbsalazar",
            "email": "you@example.com",
            "first_name": "First name",
            "last_name": "Last name",
            "contact_number": "09xx xxx xxxx",
            "city": "City / Province",
        }
        for name, ph in placeholders.items():
            if name in self.fields:
                self.fields[name].widget.attrs["placeholder"] = ph
        self._style()

    def clean_role(self):
        role = self.cleaned_data.get("role")
        if role not in {"seeker", "employer"}:
            raise ValidationError("Invalid role selection.")
        return role


class LoginForm(_FormControlMixin, forms.Form):
    identifier = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self._style()

    def clean(self):
        cleaned = super().clean()
        identifier = cleaned.get("identifier")
        password = cleaned.get("password")
        if not identifier or not password:
            return cleaned

        # Try email → username; fallback to username directly.
        try:
            user_obj = User.objects.get(email__iexact=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid credentials.")
        self.user = user
        return cleaned

    def get_user(self):
        return self.user
