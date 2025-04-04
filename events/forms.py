from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'start_date', 'end_date', 
            'location', 'mode', 'organizer', 'color', 'capacity'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields accessible with proper labels and aria attributes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['aria-required'] = 'true' if field.required else 'false'
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        # Validate that end date is after start date
        if start_date and end_date and end_date <= start_date:
            self.add_error('end_date', _('End date must be after start date'))
        
        return cleaned_data
