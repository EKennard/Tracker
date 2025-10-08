from django import forms
from .models import FertilityLog

class FertilityLogForm(forms.ModelForm):
    class Meta:
        model = FertilityLog
        fields = ['date', 'cycle_day', 'temperature', 'symptoms', 'notes']
