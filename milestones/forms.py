from django import forms
from .models import Milestone

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'description', 'target_date', 'milestone_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border rounded p-2'}),
            'description': forms.Textarea(attrs={'class': 'border rounded p-2', 'rows': 2}),
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2'}),
            'milestone_type': forms.Select(attrs={'class': 'border rounded p-2'}),
        }
