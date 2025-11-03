from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Notification(models.Model):
    profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    scheduled_for = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f"Notification for {self.profile.user.username}: {self.message}"


