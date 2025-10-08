from django.contrib import admin
from .models import HealthMetrics, ProgressPhoto, Measurement

admin.site.register(HealthMetrics)
admin.site.register(ProgressPhoto)
admin.site.register(Measurement)
