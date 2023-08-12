from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from . import models
import datetime
from django.shortcuts import render, redirect


class ProfileUpdateForm(forms.ModelForm):
    error_css_class = "error"

    class Meta:
        model = models.Profile
        exclude = ["user"]


class TenantProfileUpdateForm(forms.ModelForm):
    error_css_class = "error"

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


class MealRequestForm(forms.ModelForm):
    error_css_class = "error"

    class Meta:
        model = models.Meal
        exclude = ["tenant"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "required": True}),
            "meal_time": forms.Select(
                choices=[(0, "Lunch"), (1, "Dinner")], attrs={"required": True}
            ),
            "on": forms.CheckboxInput(),
            "extra_meal": forms.NumberInput(
                attrs={
                    "required": True,
                    "min": 0,
                    "max": 3,
                    "value": 0,
                    "id": "extra_meal",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        # should not be able to request meal for past dates
        if cleaned_data["date"] < datetime.date.today():
            raise ValidationError("You cannot request meal for past dates")

        # should not be able to request meal for today after 11am for lunch and after 5pm for dinner
        if cleaned_data["date"] == datetime.date.today():
            if datetime.datetime.now().hour > 11 and cleaned_data["meal_time"] == 0:
                raise ValidationError("You cannot request lunch after 11am")
            if datetime.datetime.now().hour > 17 and cleaned_data["meal_time"] == 1:
                raise ValidationError("You cannot request dinner after 5pm")

        # if extra meal is requested, the meal should be on
        if cleaned_data["extra_meal"] > 0 and not cleaned_data["on"]:
            raise ValidationError("You cannot request extra meal when meal is off")


class CleaningRequestForm(forms.ModelForm):
    error_css_class = "error"

    class Meta:
        model = models.CleaningRequest
        exclude = ["tenant", "status"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "required": True}),
        }

    def __init__(self, *args, **kwargs):
        self.tenant = kwargs.pop("tenant", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        # should not be able to request cleaning for past dates
        if cleaned_data["date"] <= datetime.date.today():
            raise ValidationError(
                "You have to request cleaning at least one day in advance"
            )

        # TODO: only one request per day for the same room
        # ISSUE: can't access tenant from here
        # NOTE: might need do this in the view
        cleaning_reqs = models.CleaningRequest.objects.filter(
            date=cleaned_data["date"], tenant__room=self.tenant.room
        )

        if cleaning_reqs.exists():
            raise ValidationError("You have already requested cleaning for this date")

        # should not exceed the cleaning slot limit
        count = models.CleaningRequest.objects.filter(
            date=cleaned_data["date"], slot=cleaned_data["slot"]
        ).count()
        if count >= self.tenant.room.branch.cleaning_slot_limit:
            raise ValidationError("This cleaning slot is already full")


class RepairRequestForm(forms.ModelForm):
    error_css_class = "error"

    class Meta:
        model = models.RepairRequest
        fields = ["description"]
        widgets = {
            "description": forms.Textarea(attrs={"required": True}),
        }


class LaundryRequestForm(forms.ModelForm):
    error_css_class = "error"

    class Meta:
        model = models.LaundryRequest
        exclude = ["tenant", "status"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "required": True}),
        }


class LaundryItemForm(forms.ModelForm):
    error_css_class = "error"

    class Meta:
        model = models.LaundryItem
        fields = ["item", "color"]
