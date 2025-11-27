from django import forms
from .models import HealthMetrics, Measurement

class HealthMetricsForm(forms.ModelForm):
    class Meta:
        model = HealthMetrics
        fields = ['date', 'weight', 'body_fat_percentage', 'basal_metabolic_rate', 'daily_caloric_needs']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'border rounded p-2',
                'title': 'Select any date - perfect for adding historic data!'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'border rounded p-2',
                'step': '0.1',
                'placeholder': 'Required'
            }),
            'body_fat_percentage': forms.NumberInput(attrs={
                'class': 'border rounded p-2',
                'step': '0.1',
                'placeholder': 'Optional'
            }),
            'basal_metabolic_rate': forms.NumberInput(attrs={
                'class': 'border rounded p-2',
                'placeholder': 'Optional'
            }),
            'daily_caloric_needs': forms.NumberInput(attrs={
                'class': 'border rounded p-2',
                'placeholder': 'Optional'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set today's date as default
        if not self.instance.pk and 'date' not in self.data:
            from datetime import date
            self.initial['date'] = date.today()
        
        # Make most fields optional - only weight is required
        self.fields['basal_metabolic_rate'].required = False
        self.fields['daily_caloric_needs'].required = False
        self.fields['body_fat_percentage'].required = False

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
