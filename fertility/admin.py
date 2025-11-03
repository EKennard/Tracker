from django.contrib import admin
from .models import Cycle, Fertility, Pregnancy, FertilityLog

admin.site.register(Cycle)
admin.site.register(Fertility)
admin.site.register(Pregnancy)
admin.site.register(FertilityLog)
