from django import forms
from .models import Itinerary
from django.forms import modelformset_factory

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
