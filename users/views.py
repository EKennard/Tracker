from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from meals.models import NutritionLog
from metrics.models import HealthMetrics, Measurement
from milestones.models import Milestone
from habits.models import HabitLog
from exercise.models import ExerciseLog
from fertility.models import FertilityLog

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Friendship
from .forms import FriendRequestForm, UserProfileForm
from .decorators import profile_required

# Create your views here.

@login_required
def dashboard(request):
    # Check if user has a profile, if not redirect to profile creation
    try:
        profile = request.user.userprofile
        
        # Check if this is the user's first login by checking if they have any activity
        has_activity = (
            NutritionLog.objects.filter(profile=profile).exists() or
            HealthMetrics.objects.filter(user_profile=profile).exists() or
            Measurement.objects.filter(profile=profile).exists() or
            Milestone.objects.filter(profile=profile).exists() or
            HabitLog.objects.filter(profile=profile).exists() or
            ExerciseLog.objects.filter(profile=profile).exists() or
            FertilityLog.objects.filter(profile=profile).exists()
        )
        
        # Show welcome message only if they have no activity yet
        if not has_activity and not request.session.get('welcomed', False):
            messages.success(
                request, 
                f'Welcome to GetLizzyFit, {request.user.username}! 🎉 '
                'Start your wellness journey by logging your first meal, workout, or metric. '
                'Explore the navigation menu to track your progress!'
            )
            request.session['welcomed'] = True
            
    except UserProfile.DoesNotExist:
        return redirect('create_profile')
    
    # Get all metrics for progress tracking
    all_metrics = HealthMetrics.objects.filter(user_profile=profile).order_by('date')
    
    # Helper function to convert weight for display based on user preference
    def convert_weight_for_display(weight_in_lb):
        if profile.weight_unit == 'st':
            # Convert pounds to stones (1 stone = 14 pounds)
            return float(weight_in_lb) / 14.0
        return float(weight_in_lb)
    
    # Calculate weight progress
    current_weight = None
    current_weight_display = None
    weight_lost = 0
    weight_progress_percent = 0
    if all_metrics.exists():
        latest_metric = all_metrics.last()
        current_weight = latest_metric.weight  # stored in lb
        current_weight_display = convert_weight_for_display(current_weight)
        weight_lost = convert_weight_for_display(profile.starting_weight - current_weight)
        
        # Calculate progress percentage if goal weight exists
        if hasattr(profile, 'goal_weight') and profile.goal_weight:
            total_to_lose = profile.starting_weight - profile.goal_weight
            if total_to_lose > 0:
                weight_progress_percent = (weight_lost / total_to_lose) * 100
    
    # Calculate BMI if we have current weight and height
    current_bmi = None
    weight_for_bmi = current_weight if current_weight else profile.starting_weight
    
    if weight_for_bmi and profile.height:
        # Convert height to meters for BMI calculation
        if profile.height_unit == 'cm':
            height_m = float(profile.height) / 100
        else:  # inches
            height_m = float(profile.height) * 0.0254
        
        # Convert weight to kg for BMI calculation (weight is stored in lb)
        weight_kg = float(weight_for_bmi) * 0.453592  # Convert lb to kg
        
        if weight_kg > 0 and height_m > 0:
            current_bmi = weight_kg / (height_m ** 2)
    
    # Get weight data for chart (last 30 entries or all if less)
    weight_data = list(all_metrics.values('date', 'weight').order_by('-date')[:30])
    weight_data.reverse()  # Oldest to newest for chart
    
    # Convert all weights for display based on user preference
    for entry in weight_data:
        entry['weight'] = convert_weight_for_display(entry['weight'])
    
    # Add starting weight as first data point
    if profile.starting_weight:
        # Get profile creation date
        start_date = profile.user.date_joined.strftime('%Y-%m-%d')
        starting_weight_display = convert_weight_for_display(profile.starting_weight)
        
        # Only add if no metrics exist OR starting weight isn't in the data
        if not weight_data:
            # No metrics yet, just add starting weight
            weight_data = [{'date': start_date, 'weight': starting_weight_display}]
        else:
            # Check if starting weight already exists in metrics
            first_weight = weight_data[0]['weight']
            if abs(float(first_weight) - float(starting_weight_display)) > 0.1:
                # Starting weight is different, add it as first point
                weight_data.insert(0, {'date': start_date, 'weight': starting_weight_display})
    
    # Convert starting weight for display
    starting_weight_display = convert_weight_for_display(profile.starting_weight)
    
    # Get proper display unit label
    display_unit = 'st' if profile.weight_unit == 'st' else profile.weight_unit
    
    # Unified activity stream - combine all activities
    from itertools import chain
    from operator import attrgetter
    
    recent_meals = NutritionLog.objects.filter(profile=profile).order_by('-date')[:10]
    recent_metrics = all_metrics.order_by('-date')[:10]
    recent_measurements = Measurement.objects.filter(profile=profile).order_by('-date')[:10]
    recent_habits = HabitLog.objects.filter(profile=profile).order_by('-date')[:10]
    recent_exercise = ExerciseLog.objects.filter(profile=profile).order_by('-date')[:10]
    
    # Add activity_type to each object for display
    for meal in recent_meals:
        meal.activity_type = 'meal'
        meal.activity_icon = '🍽️'
        meal.activity_text = f"{meal.get_meal_type_display()} ({meal.calories} kcal)"
    
    for metric in recent_metrics:
        metric.activity_type = 'metric'
        metric.activity_icon = '⚖️'
        weight_display = convert_weight_for_display(metric.weight)
        metric.activity_text = f"Weight: {weight_display:.1f} {display_unit}"
    
    for measurement in recent_measurements:
        measurement.activity_type = 'measurement'
        measurement.activity_icon = '📏'
        measurement.activity_text = f"{measurement.body_part}: {measurement.value} {measurement.unit}"
    
    for habit in recent_habits:
        habit.activity_type = 'habit'
        habit.activity_icon = '✅'
        habit.activity_text = f"{habit.habit_name}" + (f" - {habit.value} {habit.unit}" if habit.value else "")
    
    for exercise in recent_exercise:
        exercise.activity_type = 'exercise'
        exercise.activity_icon = '💪'
        exercise.activity_text = f"{exercise.get_exercise_type_display()} ({exercise.duration_minutes} min)"
    
    # Combine and sort all activities by date
    activity_stream = sorted(
        chain(recent_meals, recent_metrics, recent_measurements, recent_habits, recent_exercise),
        key=attrgetter('date'),
        reverse=True
    )[:15]  # Show last 15 activities
    
    # Activity counts
    total_meals = NutritionLog.objects.filter(profile=profile).count()
    total_workouts = ExerciseLog.objects.filter(profile=profile).count()
    total_habit_logs = HabitLog.objects.filter(profile=profile).count()
    
    return render(request, 'users/dashboard.html', {
        'profile': profile,
        'starting_weight_display': starting_weight_display,
        'current_weight': current_weight_display,
        'current_bmi': current_bmi,
        'weight_lost': weight_lost,
        'weight_progress_percent': weight_progress_percent,
        'weight_data': weight_data,
        'activity_stream': activity_stream,
        'total_meals': total_meals,
        'total_workouts': total_workouts,
        'total_habit_logs': total_habit_logs,
        'weight_unit': display_unit,
        'height_unit': profile.height_unit,
        'goal_weight': getattr(profile, 'goal', None),
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def create_profile(request):
    """Create a UserProfile for a new user"""
    # Check if profile already exists
    try:
        profile = request.user.userprofile
        return redirect('user_dashboard')
    except UserProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        
        # Debug: Print what data was received
        print("POST Data received:")
        for key, value in request.POST.items():
            print(f"  {key}: {value}")
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            # DOB is saved from the form, age is calculated in form.clean()
            profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            profile.age = form.cleaned_data.get('age', 0)  # Save the calculated age
            profile.save()
            messages.success(
                request, 
                f'Profile created successfully! Welcome to GetLizzyFit, {request.user.username}! 🎉'
            )
            return redirect('user_dashboard')
        else:
            # Debug: Print form errors
            print("Form validation errors:")
            print(form.errors)
            print("Non-field errors:")
            print(form.non_field_errors())
    else:
        form = UserProfileForm()
        # Show welcome message only on first visit to profile creation
        if not request.session.get('profile_creation_started', False):
            messages.info(
                request,
                f'Welcome {request.user.username}! 👋 Let\'s set up your profile to get started with your wellness journey.'
            )
            request.session['profile_creation_started'] = True
    
    return render(request, 'users/create_profile.html', {'form': form})


@login_required
@profile_required
def send_friend_request(request, user_id):
    to_user = UserProfile.objects.get(user__id=user_id)
    from_user = request.user.userprofile
    if from_user != to_user and not Friendship.objects.filter(from_user=from_user, to_user=to_user).exists():
        Friendship.objects.create(from_user=from_user, to_user=to_user, is_active=False)
    return redirect('user_list')

@login_required
@profile_required
def accept_friend_request(request, friendship_id):
    friendship = Friendship.objects.get(id=friendship_id, to_user=request.user.userprofile)
    friendship.is_active = True
    friendship.save()
    return redirect('user_list')

@login_required
@profile_required
def user_list(request):
    users = UserProfile.objects.exclude(user=request.user)
    my_profile = request.user.userprofile
    sent = Friendship.objects.filter(from_user=my_profile)
    received = Friendship.objects.filter(to_user=my_profile)
    return render(request, 'users/user_list.html', {
        'users': users,
        'sent': sent,
        'received': received,
    })
