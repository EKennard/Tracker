from django import forms
from users.models import Friendship, UserProfile
from datetime import date

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = []

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        label='Date of Birth',
        required=True
    )
    
    # Weight fields for stones/pounds
    weight_stones = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Stones'}),
        label='Stones'
    )
    weight_pounds_extra = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Pounds', 'step': '0.1'}),
        label='Pounds'
    )
    
    # Height fields for feet/inches
    height_feet = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Feet'}),
        label='Feet'
    )
    height_inches = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Inches', 'step': '0.1'}),
        label='Inches'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make starting_weight and height not required since they're conditionally required
        self.fields['starting_weight'].required = False
        self.fields['height'].required = False
    
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'sex', 'starting_weight', 'weight_unit', 
                  'height', 'height_unit', 'activity_level', 'goal', 
                  'deadline', 'distance_unit', 'is_public']
        widgets = {
            'starting_weight': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'height': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'goal': forms.TextInput(attrs={'placeholder': 'e.g., Lose 10kg, Run 5km', 'class': 'form-input'}),
            'weight_unit': forms.Select(attrs={'class': 'form-input'}),
            'height_unit': forms.Select(attrs={'class': 'form-input'}),
            'distance_unit': forms.Select(attrs={'class': 'form-input'}),
            'sex': forms.Select(attrs={'class': 'form-input'}),
            'activity_level': forms.Select(attrs={'class': 'form-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        weight_unit = cleaned_data.get('weight_unit')
        height_unit = cleaned_data.get('height_unit')
        
        # Calculate age from DOB
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            cleaned_data['age'] = age
        
        # Handle weight based on unit
        if weight_unit == 'st':
            # Using stones - convert to pounds for storage
            stones = cleaned_data.get('weight_stones')
            pounds = cleaned_data.get('weight_pounds_extra', 0)
            if stones is None or stones == '':
                raise forms.ValidationError('Please enter weight in stones.')
            # Convert to total pounds, then store
            total_pounds = (stones * 14) + (pounds or 0)
            cleaned_data['starting_weight'] = total_pounds
            # Update weight_unit to 'lb' since we're storing in pounds
            cleaned_data['weight_unit'] = 'lb'
        else:
            # Using kg or lb - require starting_weight field
            if not cleaned_data.get('starting_weight'):
                raise forms.ValidationError('Please enter your starting weight.')
        
        # Handle height based on unit
        if height_unit == 'in':
            # Check if user provided feet/inches (which means they want feet/inches display)
            feet = cleaned_data.get('height_feet')
            inches = cleaned_data.get('height_inches', 0)
            if feet is not None and feet != '':
                # Using feet/inches - convert to total inches for storage
                total_inches = (feet * 12) + (inches or 0)
                cleaned_data['height'] = total_inches
                # Keep height_unit as 'in' since we're storing in inches
            elif not cleaned_data.get('height'):
                raise forms.ValidationError('Please enter height in feet.')
        else:
            # Using cm - require height field
            if not cleaned_data.get('height'):
                raise forms.ValidationError('Please enter your height.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Age is set in clean()
        if hasattr(self, 'cleaned_data'):
            instance.age = self.cleaned_data.get('age', instance.age)
        if commit:
            instance.save()
        return instance
