from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('fertility/', include('fertility.urls')),
    path('users/', include('users.urls')),
    path('meals/', include('meals.urls')),
    path('metrics/', include('metrics.urls')),
    path('social/', include('social.urls')),
    path('notifications/', include('notifications.urls')),
    path('exercise/', include('exercise.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
