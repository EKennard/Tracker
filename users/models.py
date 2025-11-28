from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

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

    # Social features
    personal_key = models.CharField(max_length=12, unique=True, blank=True, help_text='Unique code for others to find you')
    is_public = models.BooleanField(default=False, help_text='Allow others to view your progress and milestones')

    def save(self, *args, **kwargs):
        # Generate personal key if not exists
        if not self.personal_key:
            self.personal_key = self.generate_unique_key()
        super().save(*args, **kwargs)
    
    def generate_unique_key(self):
        """Generate a unique 12-character key for user discovery"""
        while True:
            key = str(uuid.uuid4().hex)[:12].upper()
            if not UserProfile.objects.filter(personal_key=key).exists():
                return key

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def get_friends(self):
        """Get all accepted friends"""
        sent = Friendship.objects.filter(from_user=self, accepted=True).values_list('to_user', flat=True)
        received = Friendship.objects.filter(to_user=self, accepted=True).values_list('from_user', flat=True)
        friend_ids = list(sent) + list(received)
        return UserProfile.objects.filter(id__in=friend_ids)
    
class Friendship(models.Model):
    from_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='friendships_sent')
    to_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='friendships_received')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
    
    def __str__(self):
        return f"{self.from_user.user.username} -> {self.to_user.user.username} ({'Accepted' if self.accepted else 'Pending'})"

class UserSettings(models.Model):
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, related_name='settings')
    dark_mode = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    daily_summary = models.BooleanField(default=False)

    def __str__(self):
        return f"Settings for {self.profile.user.username}"