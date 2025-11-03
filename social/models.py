from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Group(models.Model):
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField('users.UserProfile', related_name='groups')
    def __str__(self):
        return self.name

class Challenge(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='challenges')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.name} ({self.group.name})"