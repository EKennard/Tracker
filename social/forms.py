from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded p-2'}),
            'description': forms.Textarea(attrs={'class': 'border rounded p-2', 'rows': 2}),
        }
