from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "user_type")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "user_type")


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = CustomUser
