from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import FertilityLog
from .forms import FertilityLogForm
from users.decorators import profile_required

@login_required
@profile_required
def fertility_log(request):
    profile = request.user.userprofile
    logs = profile.fertility_logs.all().order_by('-date')
    if request.method == 'POST':
        form = FertilityLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.profile = profile
            log.save()
            return redirect('fertility_log')
    else:
        form = FertilityLogForm()
    return render(request, 'fertility/fertility_log.html', {'form': form, 'logs': logs})
