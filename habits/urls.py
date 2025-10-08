from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.habits_log, name='habits_log'),
]
