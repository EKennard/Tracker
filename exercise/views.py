from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ExerciseLogForm
from .models import ExerciseLog

# Create your views here.

@login_required
def exercise_log(request):
    profile = request.user.userprofile
    logs = ExerciseLog.objects.filter(profile=profile).order_by('-date')
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.profile = profile
            log.save()
            return redirect('exercise_log')
    else:
        form = ExerciseLogForm()
    return render(request, 'exercise/exercise_log.html', {'form': form, 'logs': logs})
