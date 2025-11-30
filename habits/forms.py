from django import forms
from .models import HabitLog

class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ['habit_name', 'date', 'value', 'unit']
        widgets = {
            'habit_name': forms.TextInput(attrs={'class': 'border rounded p-2'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2'}),
            'value': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'unit': forms.TextInput(attrs={'class': 'border rounded p-2'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional
        for field in self.fields.values():
            field.required = False
