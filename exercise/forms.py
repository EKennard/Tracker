from django import forms
from .models import ExerciseLog

class ExerciseLogForm(forms.ModelForm):
    # Override distance_unit to use profile-compatible choices
    DISTANCE_CHOICES = [
        ('km', 'Kilometres'),
        ('mi', 'Miles'),
    ]
    distance_unit = forms.ChoiceField(
        choices=DISTANCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'border rounded p-2'})
    )
    
    class Meta:
        model = ExerciseLog
        fields = ['date', 'exercise_type', 'duration_minutes', 'distance_logged', 'distance_unit', 'rating', 'intensity', 'emoji', 'calories_burned', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2'}),
            'exercise_type': forms.Select(attrs={'class': 'border rounded p-2'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'distance_logged': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'rating': forms.Select(attrs={'class': 'border rounded p-2'}),
            'intensity': forms.Select(attrs={'class': 'border rounded p-2'}),
            'emoji': forms.Select(attrs={'class': 'border rounded p-2'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'notes': forms.Textarea(attrs={'class': 'border rounded p-2', 'rows': 2}),
        }
