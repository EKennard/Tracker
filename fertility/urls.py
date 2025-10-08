from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CycleViewSet, FertilityViewSet, PregnancyViewSet

router = DefaultRouter()
router.register(r'cycles', CycleViewSet)
router.register(r'fertility', FertilityViewSet)
router.register(r'pregnancy', PregnancyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
