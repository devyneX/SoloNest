from django import forms
from . import models


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ["user"]


class TenantProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ["user"]
        widget = {
            "nid": forms.TextInput(attrs={"required": True}),
            "birth_certificate_no": forms.TextInput(attrs={"required": True}),
            "phone_no": forms.TextInput(attrs={"required": True}),
            "blood_group": forms.TextInput(attrs={"required": True}),
            "emergency_contact": forms.TextInput(attrs={"required": True}),
        }


class MealForm(forms.ModelForm):
    class Meta:
        model = models.Meal
        exclude = ["tenant", "date"]
        widgets = {
            "meal_time": forms.Select(
                choices=[(0, "Lunch"), (1, "Dinner")], attrs={"required": True}
            ),
        }
