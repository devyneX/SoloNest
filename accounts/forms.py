from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")
