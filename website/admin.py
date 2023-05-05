from django.contrib import admin
from .models import Record, Person, Frame, Slot, SlotValue, Example
from .models import User

admin.site.register(Record)
admin.site.register(User)
admin.site.register(Person)
admin.site.register(Frame)
admin.site.register(Slot)
admin.site.register(SlotValue)
admin.site.register(Example)