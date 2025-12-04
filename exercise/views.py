from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ExerciseLogForm
from .models import ExerciseLog
from users.decorators import profile_required

# Create your views here.

@login_required
@profile_required
def exercise_log(request):
    profile = request.user.userprofile
    logs = ExerciseLog.objects.filter(profile=profile).order_by('-date')
    
    # Helper function to convert distance for display
    def convert_distance_for_display(distance, stored_unit):
        """Convert distance from stored unit to user's preferred unit"""
        if not distance:
            return None
        
        # Units are now consistent (km/mi), so check if conversion needed
        if not stored_unit or stored_unit == profile.distance_unit:
            return float(distance)
        
        # Convert between km and mi
        if stored_unit == 'km' and profile.distance_unit == 'mi':
            # km to miles (1 km = 0.621371 mi)
            return float(distance) * 0.621371
        elif stored_unit == 'mi' and profile.distance_unit == 'km':
            # miles to km (1 mi = 1.60934 km)
            return float(distance) * 1.60934
        
        return float(distance)
    
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST, user_profile=profile)
        if form.is_valid():
            log = form.save(commit=False)
            log.profile = profile
            log.save()
            return redirect('exercise_log')
    else:
        # Pre-populate form with user's preferred distance unit
        form = ExerciseLogForm(initial={'distance_unit': profile.distance_unit}, user_profile=profile)
    
    # Add converted distance display to each log
    for log in logs:
        log.distance_display = convert_distance_for_display(log.distance_logged, log.distance_unit)
    
    return render(request, 'exercise/exercise_log.html', {
        'form': form, 
        'logs': logs,
        'distance_unit': profile.distance_unit,
    })
