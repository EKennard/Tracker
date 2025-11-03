from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('register/', views.register, name='register'),
    path('users/', views.user_list, name='user_list'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:friendship_id>/', views.accept_friend_request, name='accept_friend_request'),
]
