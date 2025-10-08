from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.milestones_list, name='milestones_list'),
    path('share/<str:app_label>.<str:model_name>/<int:object_id>/',
         __import__('milestones.share_views').share_views.share_item,
         name='share_item'),
]
