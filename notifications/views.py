from django.shortcuts import render
from django.http import HttpResponse
from .forms import NotificationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Notification

# Create your views here.

@login_required
def notifications_list(request):
    profile = request.user.userprofile
    notifications = Notification.objects.filter(profile=profile).order_by('-created_at')
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notif = form.save(commit=False)
            notif.profile = profile
            notif.save()
            return redirect('notifications_list')
    else:
        form = NotificationForm()
    return render(request, 'notifications/notifications_list.html', {'form': form, 'notifications': notifications})
