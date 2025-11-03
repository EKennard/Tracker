
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class HealthMetrics(models.Model):
    user_profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
        # activity_level field removed: no users.ActivityLevel model exists
    basal_metabolic_rate = models.FloatField()
    daily_caloric_needs = models.FloatField()
    body_fat_percentage = models.FloatField()

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.date}"

class ProgressPhoto(models.Model):
    profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='progress_photos/')
    date_uploaded = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=50, blank=True, null=True, help_text='e.g. Start, Midway, Goal')
    is_public = models.BooleanField(default=False, help_text='Allow this photo to be visible to others')

    def __str__(self):
        return f"{self.profile.user.username} - Photo on {self.date_uploaded}"

class Measurement(models.Model):
    profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='measurements')
    date = models.DateField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    body_part = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=10, default='cm')
    def __str__(self):
        return f"{self.body_part} for {self.profile.user.username} on {self.date}"

