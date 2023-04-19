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


class Frame(models.Model):
    frame_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.frame_name}"


class Slot(models.Model):
    slot_name = models.CharField(max_length=200)
    frames = models.ManyToManyField(Frame, through='Example')

    def __str__(self):
        return f"{self.slot_name}"



class SlotValue(models.Model):
    value_name = models.CharField(max_length=200, null=True)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.value_name}"



class Example(models.Model):
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True)
    slot_value = models.ForeignKey(SlotValue, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.frame} - {self.slot} - {self.slot_value}'


class Dialog(models.Model):
    slot_name = models.CharField(max_length=255)  # Tên của slot
    slot_value = models.CharField(max_length=255)  # Giá trị của slot
    answer = models.CharField(max_length=3)  # Câu trả lời của người dùng (yes/no)

    def __str__(self):
        return f"{self.slot_name}: {self.slot_value} - {self.answer}"