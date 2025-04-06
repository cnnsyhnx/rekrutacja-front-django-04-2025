from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField

from django.contrib.auth.models import User

class Event(models.Model):
    MODE_CHOICES = (
        ('remote', _('Zdalnie')),
        ('in_person', _('Stacjonarnie')),
    )
    
    name = models.CharField(_('Nazwa'), max_length=200)
    description = models.TextField(_('Opis'))
    start_date = models.DateTimeField(_('Data rozpoczęcia'))
    end_date = models.DateTimeField(_('Data zakończenia'))
    location = models.CharField(_('Lokalizacja'), max_length=200)
    mode = models.CharField(_('Tryb'), max_length=10, choices=MODE_CHOICES, default='in_person')
    organizer = models.CharField(_('Organizator'), max_length=200)
    color = ColorField(_('Kolor w kalendarzu'), default='#003d7c')
    capacity = models.PositiveIntegerField(_('Pojemność'), validators=[MinValueValidator(1)])
    registered = models.PositiveIntegerField(_('Zarejestrowani uczestnicy'), default=0)
    created_at = models.DateTimeField(_('Utworzono'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Zaktualizowano'), auto_now=True)
    participants = models.ManyToManyField(User, through='EventRegistration', related_name='events')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events', null=True, blank=True, verbose_name=_('Twórca'))
    
    class Meta:
        verbose_name = _('Wydarzenie')
        verbose_name_plural = _('Wydarzenia')
        ordering = ['start_date']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})
    
    def is_full(self):
        return self.registered >= self.capacity
    
    def get_percent_full(self):
        if self.capacity == 0:
            return 100
        return int((self.registered / self.capacity) * 100)
    
    def register_user(self, user):
        """
        Register a user for this event if there's still room
        """
        if not self.is_full() and not EventRegistration.objects.filter(event=self, user=user).exists():
            EventRegistration.objects.create(event=self, user=user)
            self.registered += 1
            self.save()
            return True
        return False
    
    def unregister_user(self, user):
        """
        Unregister a user from this event
        """
        try:
            registration = EventRegistration.objects.get(event=self, user=user)
            registration.delete()
            self.registered -= 1
            self.save()
            return True
        except EventRegistration.DoesNotExist:
            return False


class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_registrations')
    registered_at = models.DateTimeField(_('Data rejestracji'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Rejestracja na wydarzenie')
        verbose_name_plural = _('Rejestracje na wydarzenia')
        unique_together = ('user', 'event')
        
    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
    
    def available_seats(self):
        return max(0, self.event.capacity - self.event.registered)
    
    def is_upcoming(self):
        from django.utils import timezone
        return self.event.start_date > timezone.now()
