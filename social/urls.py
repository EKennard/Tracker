from django.urls import path
from . import views

urlpatterns = [
    # Global feed
    path('feed/', views.global_feed, name='global_feed'),
    
    # User search and friend requests
    path('search/', views.search_users, name='search_users'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    path('send-friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:friendship_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline-friend-request/<int:friendship_id>/', views.decline_friend_request, name='decline_friend_request'),
    
    # Groups
    path('groups/', views.groups, name='groups'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/invite/<int:user_id>/', views.invite_to_group, name='invite_to_group'),
    path('accept-group-invitation/<int:invitation_id>/', views.accept_group_invitation, name='accept_group_invitation'),
    path('decline-group-invitation/<int:invitation_id>/', views.decline_group_invitation, name='decline_group_invitation'),
]
