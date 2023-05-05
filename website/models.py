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

    class Meta:
        db_table = "user"
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
    username = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "pesonal"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Frame(models.Model):
    frame_name = models.CharField(max_length=200)

    class Meta:
        db_table = "frame"

    def __str__(self):
        return f"{self.frame_name}"


class Slot(models.Model):
    slot_name = models.CharField(max_length=200)
    frames = models.ManyToManyField(Frame, through='Example')
    class Meta:
        db_table = "slot"

    def __str__(self):
        return f"{self.slot_name}"



class SlotValue(models.Model):
    value_name = models.CharField(max_length=200, null=True)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)

    class Meta:
        db_table = "slot_value"

    def __str__(self):
        return f"{self.value_name}"



class Example(models.Model):
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True)
    slot_value = models.ForeignKey(SlotValue, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "example"

    def __str__(self):
        return f'{self.frame} - {self.slot} - {self.slot_value}'


class Custom(models.Model):
    custom_date = models.DateField(blank=True, null=True)
    custom_quality = models.IntegerField(blank=True, null=True)
    custom_desc = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "custom"

class Docs(models.Model):
    doc_name = models.CharField(max_length=20, blank=True, null=True)
    doc_desc = models.CharField(max_length=20, blank=True, null=True)
    doc_location = models.CharField(max_length=20, blank=True, null=True)
    doc_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "docs"


class Equipment(models.Model):
    equipment_name = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        db_table = "equipment"


class Ic(models.Model):
    # operation = models.ForeignKey('Operation', on_delete=models.CASCADE, blank=True, null=True)
    custom = models.ForeignKey(Custom, on_delete=models.CASCADE, blank=True, null=True)
    doc = models.ForeignKey(Docs, on_delete=models.CASCADE, blank=True, null=True)
    ic_type = models.CharField(max_length=20, blank=True, null=True)
    ic_amount = models.IntegerField(blank=True, null=True)
    ic_example = models.ForeignKey(Example, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "Ic"


class Supply(models.Model):
    supply_name = models.CharField(max_length=20, blank=True, null=True)
    supply_flow = models.IntegerField(blank=True, null=True)
    supply_cost = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "supply"

class Operation(models.Model):
    equipment_id = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, blank=True, null=True)
    operation_time = models.DateField(blank=True, null=True)
    operation_name = models.CharField(max_length=20, blank=True, null=True)
    ic = models.ForeignKey(Ic, on_delete=models.CASCADE, blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "operation"
