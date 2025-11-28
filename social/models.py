from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='created_groups', null=True, blank=True)
    members = models.ManyToManyField('users.UserProfile', related_name='groups', blank=True)
    is_public = models.BooleanField(default=False, help_text='Public groups appear in search')
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class GroupInvitation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='invitations')
    from_user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='group_invites_sent')
    to_user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='group_invites_received')
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('group', 'to_user')
    
    def __str__(self):
        return f"Invite to {self.to_user.user.username} for {self.group.name}"

class GlobalActivity(models.Model):
    """Global activity feed for public users"""
    ACTIVITY_TYPES = [
        ('weight', 'Weight Log'),
        ('exercise', 'Exercise Log'),
        ('meal', 'Meal Log'),
        ('habit', 'Habit Log'),
        ('milestone', 'Milestone'),
        ('measurement', 'Measurement'),
    ]
    
    profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='global_activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='📊')
    
    # Generic foreign key to the actual activity object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.activity_type} - {self.created_at}"

class Challenge(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='challenges')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.group.name})"