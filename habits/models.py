from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class HabitLog(models.Model):
	profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='habit_logs')
	habit_name = models.CharField(max_length=100)
	date = models.DateField(default=timezone.now)
	modified_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)
	value = models.FloatField(blank=True, null=True)
	unit = models.CharField(max_length=20, blank=True, null=True)
	def __str__(self):
		return f"{self.habit_name} for {self.profile.user.username} on {self.date}"
from django.db import models
from django.utils import timezone