from django.db import models
from django.contrib.auth.models import User

class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

class Fertility(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ovulation_date = models.DateField(null=True, blank=True)
    fertile_window_start = models.DateField(null=True, blank=True)
    fertile_window_end = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

class Pregnancy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    weeks_pregnant = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

class FertilityLog(models.Model):
    profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='fertility_logs')
    date = models.DateField()
    cycle_day = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.date}"