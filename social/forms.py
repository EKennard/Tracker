from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded p-2'}),
            'description': forms.Textarea(attrs={'class': 'border rounded p-2', 'rows': 2}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5'}),
        }
