from django import forms
from .models import FertilityLog

class FertilityLogForm(forms.ModelForm):
    class Meta:
        model = FertilityLog
        fields = ['date', 'cycle_day', 'temperature', 'symptoms', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'cycle_day': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.1'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
        }
