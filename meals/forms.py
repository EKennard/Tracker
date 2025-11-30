from django import forms
from .models import NutritionLog

class NutritionLogForm(forms.ModelForm):
    class Meta:
        model = NutritionLog
        fields = ['date', 'meal_type', 'calories', 'protein', 'carbs', 'fats', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2'}),
            'meal_type': forms.Select(attrs={'class': 'border rounded p-2'}),
            'calories': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'protein': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'carbs': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'fats': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'description': forms.Textarea(attrs={'class': 'border rounded p-2', 'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional
        for field in self.fields.values():
            field.required = False
