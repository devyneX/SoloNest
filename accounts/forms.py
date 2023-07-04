from django import forms
from django.contrib.auth.models import User

# from .models import Tenant
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# class TenantSignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = Tenant
#         fields = (
#             "first_name",
#             "last_name",
#             "username",
#             "email",
#             "password1",
#             "password2",
#             "phone_no",
#             "blood_group",
#             "emergency_contact",
#             "meal_default",
#         )

#     def save(self, commit=True):
#         tenant = super(TenantSignUpForm, self).save(commit=False)
#         tenant.phone_no = self.cleaned_data["phone_no"]
#         tenant.blood_group = self.cleaned_data["blood_group"]
#         tenant.emergency_contact = self.cleaned_data["emergency_contact"]
#         tenant.meal_default = self.cleaned_data["meal_default"]
#         if commit:
#             tenant.save()
#         return tenant
