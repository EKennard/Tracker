from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import NotificationForm
from .models import Notification
from users.decorators import profile_required

# Create your views here.

@login_required
@profile_required
def notifications_list(request):
    profile = request.user.userprofile
    notifications = Notification.objects.filter(profile=profile).order_by('-created_at')
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notif = form.save(commit=False)
            notif.profile = profile
            notif.save()
            messages.success(request, '✅ Notification added successfully!')
            return redirect('notifications_list')
    else:
        form = NotificationForm()
    return render(request, 'notifications/notifications_list.html', {'form': form, 'notifications': notifications})
