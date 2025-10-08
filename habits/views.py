from django.shortcuts import render
from django.http import HttpResponse
from .forms import HabitLogForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import HabitLog

# Create your views here.

@login_required
def habits_log(request):
    profile = request.user.userprofile
    logs = HabitLog.objects.filter(profile=profile).order_by('-date')
    if request.method == 'POST':
        form = HabitLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.profile = profile
            log.save()
            return redirect('habits_log')
    else:
        form = HabitLogForm()
    return render(request, 'habits/habits_log.html', {'form': form, 'logs': logs})
