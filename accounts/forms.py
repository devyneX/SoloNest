from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
