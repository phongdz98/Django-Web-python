from django.template import Library

from ..models import *

register = Library()

@register.simple_tag
def get_slot_value(slot, frame):
    try:
        slot_value = slot.slotvalue_set.get(frame=frame)
        return slot_value.value_name
    except SlotValue.DoesNotExist:
        return None