from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.meal_log, name='meal_log'),
]
