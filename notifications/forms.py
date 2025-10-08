from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message', 'scheduled_for']
        widgets = {
            'message': forms.TextInput(attrs={'class': 'border rounded p-2'}),
            'scheduled_for': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'border rounded p-2'}),
        }
