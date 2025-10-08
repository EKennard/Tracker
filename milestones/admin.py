from django.contrib import admin
from .models import Milestone, Streak, Badge, Achievement, VictoryLog

admin.site.register(Milestone)
admin.site.register(Streak)
admin.site.register(Badge)
admin.site.register(Achievement)
admin.site.register(VictoryLog)
