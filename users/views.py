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
    
    recent_meals = NutritionLog.objects.filter(profile=profile).order_by('-date')[:5]
    recent_metrics = HealthMetrics.objects.filter(user_profile=profile).order_by('-date')[:3]
    recent_measurements = Measurement.objects.filter(profile=profile).order_by('-date')[:3]
    recent_milestones = Milestone.objects.filter(profile=profile).order_by('-target_date')[:3]
    recent_habits = HabitLog.objects.filter(profile=profile).order_by('-date')[:5]
    recent_exercise = ExerciseLog.objects.filter(profile=profile).order_by('-date')[:5]
    recent_fertility = FertilityLog.objects.filter(profile=profile).order_by('-date')[:5]
    return render(request, 'users/dashboard.html', {
        'recent_meals': recent_meals,
        'recent_metrics': recent_metrics,
        'recent_measurements': recent_measurements,
        'recent_milestones': recent_milestones,
        'recent_habits': recent_habits,
        'recent_exercise': recent_exercise,
        'recent_fertility': recent_fertility,
        'weight_unit': profile.weight_unit,
        'height_unit': profile.height_unit,
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
        # Show welcome message for first-time profile creation
        messages.info(
            request,
            f'Welcome {request.user.username}! 👋 Let\'s set up your profile to get started with your wellness journey.'
        )
    
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
