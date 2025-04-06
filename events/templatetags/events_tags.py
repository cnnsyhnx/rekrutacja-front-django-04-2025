from django import template
from events.models import EventRegistration

register = template.Library()

@register.filter
def contains(registrations, user):
    """Check if a user is in an event's registrations list"""
    if not user.is_authenticated:
        return False
    
    for registration in registrations:
        if registration.user == user:
            return True
    return False
