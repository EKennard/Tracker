from django import forms
from django.contrib.contenttypes.models import ContentType
from .shareditem import SharedItem
from .models import UserProfile

class ShareItemForm(forms.Form):
    friends = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.none(), widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['friends'].queryset = user.userprofile.friendships_sent.filter(is_active=True).values_list('to_user', flat=True)
        self.fields['friends'].queryset = UserProfile.objects.filter(id__in=self.fields['friends'].queryset)
