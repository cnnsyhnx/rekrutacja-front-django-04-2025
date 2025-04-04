from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField

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
    
    def available_seats(self):
        return max(0, self.capacity - self.registered)
    
    def is_upcoming(self):
        from django.utils import timezone
        return self.start_date > timezone.now()
