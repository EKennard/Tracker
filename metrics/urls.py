from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.metrics_summary, name='metrics_summary'),
]
