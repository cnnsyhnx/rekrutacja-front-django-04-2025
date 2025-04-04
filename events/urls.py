from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('events/monthly/', views.MonthlyEventsView.as_view(), name='monthly_events'),
    path('events/monthly/<int:year>/<int:month>/', views.MonthlyEventsView.as_view(), name='monthly_events_date'),
]
