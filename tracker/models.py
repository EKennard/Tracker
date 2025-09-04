from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ACTIVITY_LEVEL_CHOICES = [
    ('sedentary', 'Sedentary'),
    ('lightly_active', 'Lightly Active'),
    ('moderately_active', 'Moderately Active'),
    ('very_active', 'Very Active'),
    ('extra_active', 'Extra Active'),
    ('professional_athlete', 'Professional Athlete'),]


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/',
                                        blank=True, null=True)
    age = models.IntegerField()
    SEX_CHOICES = [('male', 'Male'), ('female', 'Female')]
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    starting_weight = models.DecimalField()
    height = models.DecimalField()
    activity_level = ACTIVITY_LEVEL_CHOICES, models.CharField(max_length=50)
    goal = models.CharField(max_length=50, blank=True, null=True)
    deadline = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    weight_unit = models.DecimalField(max_length=10, choices=[
        ('kg', 'Kilograms'), ('lb', 'Pounds')], default='kg')
    distance_unit = models.DecimalField(max_length=10, choices=[
        ('km', 'Kilometres'), ('mi', 'Miles')], default='km')
    height_unit = models.DecimalField(max_length=10, choices=[
        ('cm', 'Centimetres'), ('ft', 'Feet/Inches')], default='cm')


class HealthMetrics(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    height = models.DecimalField()
    weight = models.DecimalField()
    activity_level = ACTIVITY_LEVEL_CHOICES, models.CharField(max_length=50)
    basal_metabolic_rate = models.FloatField()
    daily_caloric_needs = models.FloatField()
    body_fat_percentage = models.FloatField()


def __str__(self):
    return f"{self.user_profile.user.user_name} - {self.date}"


class NutritionLog(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    meal_type = MEAL_TYPE_CHOICES, models.CharField(max_length=50)
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f"{self.profile.user_name} - {self.meal_type} on {self.date}"


class ExerciseLog(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    EXERCISE_TYPE_CHOICES = [
        ('Cardio'), [
            ('running', 'Running'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('walking', 'Walking'),
            ('rowing', 'Rowing'),
            ('jump_rope', 'Jump Rope'),
            ('aerobics', 'Aerobics'),
            ('other', 'Other Cardio'),
        ]
        ('Strength Training'), [
            ('Weightlifting'),
            ('bodyweight', 'Bodyweight Exercises'),
            ('resistance_bands', 'Resistance Bands'),
            ('circuit_training', 'Circuit Training'),
            ('crossfit', 'CrossFit'),
            ('powerlifting', 'Powerlifting'),
            ('other', 'Other Strength Training'),
        ]
        ('Flexibility & Ballance'), [
            ('yoga', 'Yoga'),
            ('pilates', 'Pilates'),
            ('tai_chi', 'Tai Chi'),
            ('other', 'Other Balance Training'),
        ]
    ]
    exercise_type = EXERCISE_TYPE_CHOICES, models.CharField(max_length=100)
    duration_minutes = models.DecimalField()
    DISTANCE_LOGGED_CHOICES = [
        ('miles', 'Miles'), ('kilometers', 'Kilometers')]
    distance_unit = DISTANCE_LOGGED_CHOICES, models.CharField(
        max_length=20, blank=True, null=True)
    distance_logged = models.DecimalField(null=True, blank=True)
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]
    rating = models.IntegerField(choices=RATING_CHOICES)
    INTENSITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    intensity = models.CharField(max_length=50)
    EMOJI_CHOICES = [
        ('😀', 'Very Satisfied'),
        ('🙂', 'Satisfied'),
        ('😐', 'Neutral'),
        ('🙁', 'Dissatisfied'),
        ('😫', 'Exhausted'),
    ]
    emoji = models.CharField(
        max_length=2, choices=EMOJI_CHOICES, blank=True, null=True)
    calories_burned = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return (
            f"{self.profile.user_name} - {self.exercise_type} on {self.date}"
        )


class ProgressPhoto(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='progress_photos/')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.profile.user_name} - Photo on {self.date_uploaded}"
