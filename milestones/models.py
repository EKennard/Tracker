from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Milestone(models.Model):
    profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_achieved = models.DateField(blank=True, null=True)
    target_date = models.DateField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_custom = models.BooleanField(default=False)
    milestone_type = models.CharField(
        max_length=50,
        choices=[
            ('weight', 'Weight Goal'),
            ('measurement', 'Measurement Goal'),
            ('habit', 'Habit Streak'),
            ('fitness', 'Fitness Achievement'),
            ('photo', 'Photo Comparison'),
            ('custom', 'Custom'),
        ],
        default='custom'
    )
    def __str__(self):
        return f"{self.title} ({self.profile.user.username})"


class Streak(models.Model):
    profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='streaks')
    habit_name = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    length = models.IntegerField(help_text='Length of streak in days')
    def __str__(self):
        return f"{self.habit_name} streak for {self.profile.user.username} ({self.length} days)"

class Badge(models.Model):
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

class Achievement(models.Model):
    profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='achievements')
    badge = models.ForeignKey('Badge', on_delete=models.CASCADE)
    date_earned = models.DateField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.profile.user.username} earned {self.badge.name}"

class VictoryLog(models.Model):
    profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='victories')
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"Victory for {self.profile.user.username} on {self.date}"
