from django import forms
from .models import ExerciseLog

class ExerciseLogForm(forms.ModelForm):
    # Separate hours and minutes fields
    duration_hours = forms.IntegerField(
        required=False,
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'border rounded p-2', 'placeholder': '0'})
    )
    duration_minutes = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=59,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'border rounded p-2', 'placeholder': '0'})
    )
    
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
        fields = ['date', 'exercise_type', 'distance_logged', 'distance_unit', 'rating', 'intensity', 'emoji', 'calories_burned', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2'}),
            'exercise_type': forms.Select(attrs={'class': 'border rounded p-2'}),
            'distance_logged': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'rating': forms.Select(attrs={'class': 'border rounded p-2'}),
            'intensity': forms.Select(attrs={'class': 'border rounded p-2'}),
            'emoji': forms.Select(attrs={'class': 'border rounded p-2'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'border rounded p-2'}),
            'notes': forms.Textarea(attrs={'class': 'border rounded p-2', 'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional
        for field in self.fields.values():
            field.required = False
        
        # If editing existing entry, split duration_minutes into hours and minutes
        if self.instance and self.instance.pk and self.instance.duration_minutes:
            total_minutes = float(self.instance.duration_minutes)
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            self.initial['duration_hours'] = hours
            self.initial['duration_minutes'] = minutes
    
    def clean(self):
        cleaned_data = super().clean()
        hours = cleaned_data.get('duration_hours', 0) or 0
        minutes = cleaned_data.get('duration_minutes', 0) or 0
        
        # Convert hours and minutes to total minutes
        total_minutes = (hours * 60) + minutes
        cleaned_data['duration_minutes'] = total_minutes
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Set duration_minutes from cleaned_data
        instance.duration_minutes = self.cleaned_data['duration_minutes']
        if commit:
            instance.save()
        return instance
