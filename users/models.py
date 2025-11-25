from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
ACTIVITY_LEVEL_CHOICES = [
    ("sedentary", "Sedentary"),
    ("lightly_active", "Lightly Active"),
    ("moderately_active", "Moderately Active"),
    ("very_active", "Very Active"),
    ("extra_active", "Extra Active"),
    ("professional_athlete", "Professional Athlete"),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField()
    SEX_CHOICES = [('male', 'Male'), ('female', 'Female')]
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    starting_weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    activity_level = models.CharField(max_length=50, choices=ACTIVITY_LEVEL_CHOICES)
    goal = models.CharField(max_length=50, blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    WEIGHT_UNIT_CHOICES = [('kg', 'Kilograms'), ('lb', 'Pounds'), ('st', 'Stones')]
    DISTANCE_UNIT_CHOICES = [('km', 'Kilometres'), ('mi', 'Miles')]
    HEIGHT_UNIT_CHOICES = [('cm', 'Centimetres'), ('in', 'Inches')]
    weight_unit = models.CharField(max_length=10, choices=WEIGHT_UNIT_CHOICES, default='kg')
    distance_unit = models.CharField(max_length=10, choices=DISTANCE_UNIT_CHOICES, default='km')
    height_unit = models.CharField(max_length=10, choices=HEIGHT_UNIT_CHOICES, default='cm')

    # Privacy control for social features
    is_public = models.BooleanField(default=False, help_text='Allow others to view your progress and milestones')

    def __str__(self):
        return f"{self.user.username} Profile"
    
class Friendship(models.Model):
    from_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='friendships_sent')
    to_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='friendships_received')
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class UserSettings(models.Model):
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, related_name='settings')
    dark_mode = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    daily_summary = models.BooleanField(default=False)


    def __str__(self):
        return f"Settings for {self.profile.user.username}"
    accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.from_user.user.username} -> {self.to_user.user.username} ({'Accepted' if self.accepted else 'Pending'})"