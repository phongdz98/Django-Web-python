from django.contrib import admin
from .models import Record, Person
from .models import User

admin.site.register(Record)
admin.site.register(User)
admin.site.register(Person)