from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *

# class TenantLogInForm(AuthenticationForm):
#     class Meta:
#         model = Tenant
#         fields = ("username", "password")


class TenantSignUpForm(UserCreationForm):
    phone_no = forms.CharField(max_length=11)
    blood_group = forms.CharField(max_length=3)
    emergency_contact = forms.CharField(max_length=11)
    meal_default = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "phone_no",
            "blood_group",
            "emergency_contact",
            "meal_default",
        )

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        tenant = Tenant.objects.create(
            user=user,
            phone_no=self.cleaned_data["phone_no"],
            blood_group=self.cleaned_data["blood_group"],
            emergency_contact=self.cleaned_data["emergency_contact"],
            meal_default=self.cleaned_data["meal_default"],
        )


class RoomRequestForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        fields = [
            "first_name",
            "last_name",
            "email",
            "single",
            "ac",
            "balcony",
            "attached_bathroom",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "single": forms.CheckboxInput(attrs={"label": "Single"}),
            "ac": forms.CheckboxInput(attrs={"label": "AC"}),
            "balcony": forms.CheckboxInput(attrs={"label": "Balcony"}),
            "attached_bathroom": forms.CheckboxInput(
                attrs={"label": "Attached Bathroom"}
            ),
        }
