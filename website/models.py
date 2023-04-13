from django.db import models
from django.contrib.auth.models import AbstractUser


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class User(AbstractUser):
    is_admin = models.BooleanField('Is Admin', default=False)
    is_technician = models.BooleanField('Is Technician', default=False)
    is_employee = models.BooleanField('Is Employee', default=False)

    def __str__(self):
        return f"{self.username}"


class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    username = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"





