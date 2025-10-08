from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.exercise_log, name='exercise_log'),
]
