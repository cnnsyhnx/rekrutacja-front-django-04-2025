import calendar
from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, FormView
from django.views.generic.dates import MonthArchiveView
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Event, EventRegistration
from .forms import EventForm, UserRegisterForm, UserLoginForm, EventRegistrationForm

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
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('index')
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create Event')
        return context
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, _('Event created successfully!'))
        return super().form_valid(form)

@method_decorator(csrf_exempt, name='dispatch')
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit Event')
        return context
    
    def dispatch(self, request, *args, **kwargs):
        """
        Öncek kontrol: kullanıcı bu etkinliği düzenleyebilir mi?
        Admin tüm eventleri düzenleyebilir, kullanıcılar sadece kendi etkinliklerini
        """
        event = self.get_object()
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_staff or request.user.is_superuser or event.creator == request.user:
            return super().dispatch(request, *args, **kwargs)
        # Yetkisiz erişim
        messages.error(request, _('Nie masz uprawnień do edycji tego wydarzenia.'))
        return redirect('event_detail', pk=event.pk)
    
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


class RegisterView(FormView):
    """View for user registration"""
    template_name = 'events/auth/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, _('Konto zostało utworzone pomyślnie! Możesz się teraz zalogować.'))
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Rejestracja')
        return context


class LoginView(FormView):
    """View for user login"""
    template_name = 'events/auth/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, _('Zalogowano pomyślnie!'))
            
            # Check if there's a next parameter to redirect to
            next_url = self.request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return super().form_valid(form)
        else:
            messages.error(self.request, _('Nieprawidłowa nazwa użytkownika lub hasło.'))
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Logowanie')
        return context


def logout_view(request):
    """View for user logout"""
    logout(request)
    messages.success(request, _('Wylogowano pomyślnie.'))
    return redirect('index')


class UserProfileView(LoginRequiredMixin, TemplateView):
    """View for user profile with registered events"""
    template_name = 'events/auth/profile.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Profil użytkownika')
        
        # Get user's registered events
        user_events = Event.objects.filter(participants=self.request.user).order_by('start_date')
        
        # Divide events into upcoming and past
        now = timezone.now()
        context['upcoming_events'] = user_events.filter(start_date__gt=now)
        context['past_events'] = user_events.filter(start_date__lte=now)
        
        return context


@method_decorator(csrf_exempt, name='dispatch')
class EventRegisterView(LoginRequiredMixin, FormView):
    """View for registering to an event"""
    template_name = 'events/event_register.html'
    form_class = EventRegistrationForm
    login_url = 'login'
    
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        context['event'] = event
        context['title'] = _('Rejestracja na wydarzenie')
        
        # Check if user is already registered
        context['is_registered'] = EventRegistration.objects.filter(
            event=event, user=self.request.user
        ).exists()
        
        return context
    
    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        
        # Check if the event is full
        if event.is_full():
            messages.error(self.request, _('Przepraszamy, wszystkie miejsca na to wydarzenie zostały zajęte.'))
            return self.form_invalid(form)
        
        # Register the user
        success = event.register_user(self.request.user)
        
        if success:
            messages.success(self.request, _('Zarejestrowano na wydarzenie pomyślnie!'))
            return super().form_valid(form)
        else:
            messages.warning(self.request, _('Jesteś już zarejestrowany na to wydarzenie.'))
            return redirect(self.get_success_url())


@method_decorator(csrf_exempt, name='dispatch')
class EventUnregisterView(LoginRequiredMixin, TemplateView):
    """View for unregistering from an event"""
    template_name = 'events/event_unregister.html'
    login_url = 'login'
    
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        context['event'] = event
        context['title'] = _('Anulowanie rejestracji')
        
        # Check if user is registered
        context['is_registered'] = EventRegistration.objects.filter(
            event=event, user=self.request.user
        ).exists()
        
        return context
    
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        
        # Unregister the user
        success = event.unregister_user(self.request.user)
        
        if success:
            messages.success(request, _('Anulowano rejestrację na wydarzenie.'))
        else:
            messages.warning(request, _('Nie byłeś zarejestrowany na to wydarzenie.'))
        
        return redirect(self.get_success_url())
