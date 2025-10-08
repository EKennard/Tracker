from django import forms
from .models import HealthMetrics, Measurement

class HealthMetricsForm(forms.ModelForm):
    class Meta:
        model = HealthMetrics
        fields = ['date', 'height', 'weight', 'basal_metabolic_rate', 'daily_caloric_needs', 'body_fat_percentage']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2'}),
            'height': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'weight': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'basal_metabolic_rate': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'daily_caloric_needs': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'body_fat_percentage': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
        }

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['date', 'body_part', 'value', 'unit']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2'}),
            'body_part': forms.TextInput(attrs={'class': 'border rounded p-2'}),
            'value': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'unit': forms.TextInput(attrs={'class': 'border rounded p-2'}),
        }
