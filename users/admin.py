from django.contrib import admin
from .models import UserProfile, Friendship, UserSettings
from .shareditem import SharedItem

admin.site.register(UserProfile)
admin.site.register(Friendship)
admin.site.register(UserSettings)
admin.site.register(SharedItem)
