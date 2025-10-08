from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class SharedItem(models.Model):
    shared_by = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='shared_items')
    shared_with = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='items_shared_with_me')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shared_by.user.username} shared {self.item} with {self.shared_with.user.username}"
