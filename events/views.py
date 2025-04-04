import calendar
from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.views.generic.dates import MonthArchiveView
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Event
from .forms import EventForm

class IndexView(TemplateView):
    template_name = 'events/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = Event.objects.filter(
            start_date__gt=timezone.now()
        ).order_by('start_date')[:6]
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

@method_decorator(csrf_exempt, name='dispatch')
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create Event')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, _('Event created successfully!'))
        return super().form_valid(form)

@method_decorator(csrf_exempt, name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit Event')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, _('Event updated successfully!'))
        return super().form_valid(form)

class MonthlyEventsView(TemplateView):
    template_name = 'events/monthly_events.html'
    
    def get_calendar_data(self, year, month):
        # Create a calendar
        cal = calendar.monthcalendar(year, month)
        
        # Get all events for this month
        events = Event.objects.filter(
            start_date__year=year,
            start_date__month=month
        ).order_by('start_date')
        
        # Calculate previous and next month
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
            
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        # Get month name
        month_name = calendar.month_name[month]
        
        # Format current month with leading zero
        current_month = f"{month:02d}"
        
        # Format today's date
        today = date.today()
        today_date = today.strftime("%Y-%m-%d")
        
        return {
            'calendar': cal,
            'events': events,
            'month_name': month_name,
            'year': year,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
            'current_month': current_month,
            'today_date': today_date,
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get year and month from URL parameters, or use current date
        year = int(self.kwargs.get('year', datetime.now().year))
        month = int(self.kwargs.get('month', datetime.now().month))
        
        # Get calendar data
        calendar_data = self.get_calendar_data(year, month)
        context.update(calendar_data)
        
        return context
