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
    starting_weight_display = convert_weight_for_display(profile.starting_weight)
    weight_lost = 0
    weight_progress_percent = 0
    
    if all_metrics.exists():
        latest_metric = all_metrics.last()
        current_weight = latest_metric.weight  # stored in lb
        current_weight_display = convert_weight_for_display(current_weight)
        weight_lost_lb = profile.starting_weight - current_weight
        weight_lost = convert_weight_for_display(weight_lost_lb)
        
        # Calculate progress percentage if goal weight exists
        if hasattr(profile, 'goal_weight') and profile.goal_weight:
            total_to_lose = profile.starting_weight - profile.goal_weight
            if total_to_lose > 0:
                weight_progress_percent = (float(weight_lost_lb) / float(total_to_lose)) * 100
    
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
    
    # Get weight data for chart - use ALL HealthMetrics entries ordered by date
    weight_data = list(all_metrics.values('date', 'weight').order_by('date'))
    
    # Debug: Print weight data
    print(f"DEBUG: Found {len(weight_data)} weight entries")
    for entry in weight_data:
        print(f"  Date: {entry['date']}, Weight (lb): {entry['weight']}")
    
    # Convert all weights for display based on user preference
    for entry in weight_data:
        entry['weight'] = convert_weight_for_display(entry['weight'])
        print(f"  After conversion: Date: {entry['date']}, Weight: {entry['weight']} {display_unit}")
    
    # If no weight data exists, show starting weight as a placeholder
    if not weight_data and profile.starting_weight:
        start_date = profile.user.date_joined.strftime('%Y-%m-%d')
        weight_data = [{'date': start_date, 'weight': starting_weight_display}]
    
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
            
            # Create initial HealthMetrics entry with starting weight
            from metrics.models import HealthMetrics
            from datetime import date
            
            HealthMetrics.objects.create(
                user_profile=profile,
                date=date.today(),
                weight=profile.starting_weight,
                height=profile.height
            )
            
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

@login_required
@profile_required
def profile_view(request):
    """View user's complete profile information"""
    profile = request.user.userprofile
    
    # Helper function to convert weight for display
    def convert_weight_for_display(weight_in_lb):
        if profile.weight_unit == 'st':
            return float(weight_in_lb) / 14.0
        elif profile.weight_unit == 'kg':
            return float(weight_in_lb) * 0.453592
        return float(weight_in_lb)
    
    # Helper function to convert height for display
    def convert_height_for_display(height_value):
        if profile.height_unit == 'in':
            # Height stored in cm, convert to inches
            return float(height_value) / 2.54
        return float(height_value)
    
    # Get weight unit display
    weight_unit = 'st' if profile.weight_unit == 'st' else profile.weight_unit
    
    # Convert starting weight for display
    starting_weight_display = f"{convert_weight_for_display(profile.starting_weight):.1f}"
    
    # Convert goal weight if exists
    goal_weight_display = None
    if hasattr(profile, 'goal_weight') and profile.goal_weight:
        goal_weight_display = f"{convert_weight_for_display(profile.goal_weight):.1f}"
    
    # Convert height for display
    height_display = f"{convert_height_for_display(profile.height):.1f}"
    
    # Get current weight and BMI from latest metrics
    all_metrics = HealthMetrics.objects.filter(user_profile=profile).order_by('date')
    current_weight_display = None
    current_bmi = None
    
    if all_metrics.exists():
        latest_metric = all_metrics.last()
        current_weight_display = f"{convert_weight_for_display(latest_metric.weight):.1f}"
        
        # Calculate BMI
        weight_for_bmi = latest_metric.weight
        if weight_for_bmi and profile.height:
            if profile.height_unit == 'cm':
                height_m = float(profile.height) / 100
            else:  # inches
                height_m = float(profile.height) * 0.0254
            
            weight_kg = float(weight_for_bmi) * 0.453592
            
            if weight_kg > 0 and height_m > 0:
                current_bmi = weight_kg / (height_m ** 2)
    
    # Get recent metrics (last 5)
    recent_metrics = all_metrics.order_by('-date')[:5]
    for metric in recent_metrics:
        metric.weight_display = f"{convert_weight_for_display(metric.weight):.1f}"
    
    # Get recent measurements (last 5)
    recent_measurements = Measurement.objects.filter(profile=profile).order_by('-date')[:5]
    
    context = {
        'profile': profile,
        'weight_unit': weight_unit,
        'starting_weight_display': starting_weight_display,
        'goal_weight_display': goal_weight_display,
        'height_display': height_display,
        'current_weight_display': current_weight_display,
        'current_bmi': current_bmi,
        'recent_metrics': recent_metrics,
        'recent_measurements': recent_measurements,
    }
    
    return render(request, 'users/profile.html', context)

@login_required
@profile_required
def edit_profile(request):
    """Edit user's profile information"""
    profile = request.user.userprofile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            updated_profile = form.save(commit=False)
            # Ensure age is saved
            updated_profile.age = form.cleaned_data.get('age', profile.age)
            updated_profile.save()
            
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('profile_view')
    else:
        # Pre-populate form with existing data
        initial_data = {}
        
        # If user's weight is stored in pounds but they use stones, show stones/pounds
        if profile.weight_unit == 'st':
            total_pounds = float(profile.starting_weight)
            stones = int(total_pounds // 14)
            pounds = total_pounds % 14
            initial_data['weight_stones'] = stones
            initial_data['weight_pounds_extra'] = round(pounds, 1)
        
        # If user's height is in inches but stored differently, convert
        if profile.height_unit == 'in':
            total_inches = float(profile.height)
            feet = int(total_inches // 12)
            inches = total_inches % 12
            initial_data['height_feet'] = feet
            initial_data['height_inches'] = round(inches, 1)
        
        form = UserProfileForm(instance=profile, initial=initial_data)
    
    return render(request, 'users/edit_profile.html', {'form': form})
