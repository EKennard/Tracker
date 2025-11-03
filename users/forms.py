from django import forms
from users.models import Friendship, UserProfile

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = []

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'sex', 'starting_weight', 'height', 'activity_level', 'goal', 
                  'deadline', 'weight_unit', 'distance_unit', 'height_unit', 'is_public']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'goal': forms.TextInput(attrs={'placeholder': 'e.g., Lose 10kg, Run 5km'}),
        }
