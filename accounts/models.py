from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_basic_user = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField()
    nid = models.CharField(max_length=13)
    birth_certificate = models.CharField(max_length=13)
    # TODO: add passport size picture
    # TODO: add nid picture
    # TODO: add birth_certificate picture
    phone_no = models.CharField(max_length=11)
    blood_group_choices = [
        ("a+", "A+ve"),
        ("a-", "A-ve"),
        ("b+", "B+ve"),
        ("b-", "B-ve"),
        ("ab+", "AB+ve"),
        ("ab-", "AB-ve"),
        ("o+", "O+ve"),
        ("o-", "O-ve"),
    ]
    blood_group = models.CharField(max_length=5, choices=blood_group_choices)
    emergency_contact = models.CharField(max_length=11)
