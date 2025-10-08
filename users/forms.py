from django import forms
from users.models import Friendship

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = []
