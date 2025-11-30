from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
ACTIVITY_LEVEL_CHOICES = [
    ('sedentary', 'Sedentary'),
    ('lightly_active', 'Lightly Active'),
    ('moderately_active', 'Moderately Active'),
    ('very_active', 'Very Active'),
    ('extra_active', 'Extra Active'),
    ('professional_athlete', 'Professional Athlete'),
]


class ExerciseLog(models.Model):
    profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    EXERCISE_TYPE_CHOICES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('rowing', 'Rowing'),
        ('jump_rope', 'Jump Rope'),
        ('aerobics', 'Aerobics'),
        ('weightlifting', 'Weightlifting'),
        ('bodyweight', 'Bodyweight Exercises'),
        ('resistance_bands', 'Resistance Bands'),
        ('circuit_training', 'Circuit Training'),
        ('crossfit', 'CrossFit'),
        ('powerlifting', 'Powerlifting'),
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('tai_chi', 'Tai Chi'),
        ('other', 'Other'),
    ]
    exercise_type = models.CharField(max_length=100, choices=EXERCISE_TYPE_CHOICES, blank=True, null=True)
    duration_minutes = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    DISTANCE_LOGGED_CHOICES = [
        ('miles', 'Miles'), ('kilometers', 'Kilometres')]
    distance_unit = models.CharField(max_length=20, choices=DISTANCE_LOGGED_CHOICES, blank=True, null=True)
    distance_logged = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    INTENSITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    intensity = models.CharField(max_length=50, choices=INTENSITY_CHOICES, blank=True, null=True)
    EMOJI_CHOICES = [
        ('😀', 'Very Satisfied'),
        ('🙂', 'Satisfied'),
        ('😐', 'Neutral'),
        ('🙁', 'Dissatisfied'),
        ('😫', 'Exhausted'),
    ]
    emoji = models.CharField(max_length=2, choices=EMOJI_CHOICES, blank=True, null=True)
    calories_burned = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.exercise_type} on {self.date}"

# StrengthSet model moved from tracker/models.py
class StrengthSet(models.Model):
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    exercise_log = models.ForeignKey('ExerciseLog', on_delete=models.CASCADE, related_name='strength_sets')
    exercise_name = models.CharField(max_length=100)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return f"{self.exercise_name} ({self.sets}x{self.reps} @ {self.weight}kg)"
from django.db import models