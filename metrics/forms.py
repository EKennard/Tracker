from django import forms
from .models import HealthMetrics, Measurement

class HealthMetricsForm(forms.ModelForm):
    # Additional fields for stones input
    weight_stones = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Stones',
            'min': '0'
        }),
        label='Stones'
    )
    weight_pounds = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Pounds',
            'min': '0',
            'max': '13.9'
        }),
        label='Pounds'
    )
    
    class Meta:
        model = HealthMetrics
        fields = ['date', 'weight']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'title': 'Select any date - perfect for adding historic data!'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Required'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        
        # Set today's date as default
        if not self.instance.pk and 'date' not in self.data:
            from datetime import date
            self.initial['date'] = date.today()
        
        # Update weight label and fields based on user's preferred unit
        if user_profile:
            weight_unit = user_profile.weight_unit
            if weight_unit == 'st':
                # For stones, hide the main weight field and show separate stones/pounds fields
                self.fields['weight'].widget = forms.HiddenInput()
                self.fields['weight'].required = False
                self.fields['weight_stones'].required = True
                self.fields['weight_pounds'].required = False
            elif weight_unit == 'kg':
                self.fields['weight'].label = 'Weight (kg)'
                self.fields['weight_stones'].widget = forms.HiddenInput()
                self.fields['weight_pounds'].widget = forms.HiddenInput()
            else:  # lb
                self.fields['weight'].label = 'Weight (lb)'
                self.fields['weight_stones'].widget = forms.HiddenInput()
                self.fields['weight_pounds'].widget = forms.HiddenInput()
    
    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        weight_stones = cleaned_data.get('weight_stones')
        weight_pounds = cleaned_data.get('weight_pounds')
        
        # If stones are provided, calculate total weight in pounds
        if weight_stones is not None:
            total_pounds = (weight_stones * 14) + (weight_pounds or 0)
            cleaned_data['weight'] = total_pounds
        
        return cleaned_data

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
