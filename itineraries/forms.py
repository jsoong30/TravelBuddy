# forms.py
from django import forms
from .models import Itinerary, Itinerary  # adjust import if needed
from .models import Itinerary, Itinerary  # Actually we need Review
from .models import Itinerary  # wait

# Correct:
from .models import Itinerary, Itinerary  # mistake

# Let's write properly:
from .models import Itinerary, Review  # ensure Review is importable

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class':'form-control'}),
            'comment': forms.Textarea(attrs={
                'class':'form-control',
                'rows':3,
                'placeholder':'What did you think?'
            }),
        }
