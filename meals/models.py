from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class NutritionLog(models.Model):
    profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES)
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f"{self.profile.user.username} - {self.meal_type} on {self.date}"

