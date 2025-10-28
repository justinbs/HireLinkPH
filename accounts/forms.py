from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ("seeker", "Job Seeker"),
        ("employer", "Employer"),
        ("admin", "Admin"),
    ]
    email = forms.EmailField(max_length=100, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "contact_number", "city", "role")

class LoginForm(forms.Form):
    identifier = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={"autofocus": True})
    )
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        identifier = cleaned.get("identifier")
        password = cleaned.get("password")
        if identifier and password:
            # allow login by email OR username
            user = None
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = authenticate(username=identifier, password=password)
            if not user:
                raise forms.ValidationError("Invalid credentials.")
            cleaned["user"] = user
        return cleaned
