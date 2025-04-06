from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Event, EventRegistration

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


class UserRegisterForm(UserCreationForm):
    """Form for user registration with additional fields"""
    email = forms.EmailField(required=True, label=_('Email'))
    first_name = forms.CharField(max_length=30, required=True, label=_('Imię'))
    last_name = forms.CharField(max_length=30, required=True, label=_('Nazwisko'))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['aria-required'] = 'true'
            
            # Translate the default error messages
            if field_name == 'password1':
                field.label = _('Hasło')
            elif field_name == 'password2':
                field.label = _('Potwierdzenie hasła')
            elif field_name == 'username':
                field.label = _('Nazwa użytkownika')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email jest już używany.'))
        return email


class UserLoginForm(AuthenticationForm):
    """Custom authentication form with styled fields"""
    username = forms.CharField(label=_('Nazwa użytkownika'))
    password = forms.CharField(label=_('Hasło'), widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['aria-required'] = 'true'


class EventRegistrationForm(forms.Form):
    """Form for registering to an event"""
    agree_to_terms = forms.BooleanField(
        required=True,
        label=_('Zapoznałem się z regulaminem i akceptuję warunki uczestnictwa'),
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'aria-required': 'true'
        })
    )
