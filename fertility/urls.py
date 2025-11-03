from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.fertility_log, name='fertility_log'),
]
