from django.shortcuts import render
from django.http import HttpResponse
from .forms import HealthMetricsForm, MeasurementForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import HealthMetrics, Measurement
from users.decorators import profile_required

# Create your views here.

@login_required
@profile_required
def metrics_summary(request):
    profile = request.user.userprofile
    metrics = HealthMetrics.objects.filter(user_profile=profile).order_by('-date')
    measurements = Measurement.objects.filter(profile=profile).order_by('-date')
    
    # Calculate BMR and caloric needs based on profile data
    # Mifflin-St Jeor Equation for BMR
    calculated_bmr = None
    calculated_calories = None
    calculated_body_fat = None
    
    if profile.height and profile.starting_weight:
        # Convert to metric for calculations
        weight_kg = float(profile.starting_weight) * 0.453592  # lb to kg
        
        if profile.height_unit == 'cm':
            height_cm = float(profile.height)
        else:  # inches
            height_cm = float(profile.height) * 2.54
        
        age = profile.age
        
        # BMR calculation using Mifflin-St Jeor
        if profile.sex == 'male':
            calculated_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:  # female
            calculated_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
        # Calculate daily caloric needs based on activity level
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9,
            'professional_athlete': 2.0,
        }
        multiplier = activity_multipliers.get(profile.activity_level, 1.2)
        calculated_calories = calculated_bmr * multiplier
        
        # Estimate body fat percentage using BMI-based formula
        # Note: This is an estimation. Actual body composition testing is more accurate.
        bmi = weight_kg / ((height_cm / 100) ** 2)
        if profile.sex == 'male':
            calculated_body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
        else:  # female
            calculated_body_fat = (1.20 * bmi) + (0.23 * age) - 5.4
        
        # Ensure body fat percentage is within reasonable bounds
        calculated_body_fat = max(5, min(50, calculated_body_fat))
    
    if request.method == 'POST':
        metrics_form = HealthMetricsForm(request.POST, prefix='metrics')
        measurement_form = MeasurementForm(request.POST, prefix='measurement')
        if metrics_form.is_valid():
            m = metrics_form.save(commit=False)
            m.user_profile = profile
            
            # Auto-fill BMR and calories if not provided
            if not m.basal_metabolic_rate and calculated_bmr:
                m.basal_metabolic_rate = int(calculated_bmr)
            if not m.daily_caloric_needs and calculated_calories:
                m.daily_caloric_needs = int(calculated_calories)
            if not m.body_fat_percentage and calculated_body_fat:
                m.body_fat_percentage = round(calculated_body_fat, 1)
            
            m.save()
            return redirect('metrics_summary')
        if measurement_form.is_valid():
            meas = measurement_form.save(commit=False)
            meas.profile = profile
            meas.save()
            return redirect('metrics_summary')
    else:
        metrics_form = HealthMetricsForm(prefix='metrics')
        measurement_form = MeasurementForm(prefix='measurement')
    
    return render(request, 'metrics/metrics_summary.html', {
        'metrics_form': metrics_form,
        'measurement_form': measurement_form,
        'metrics': metrics,
        'measurements': measurements,
        'weight_unit': profile.weight_unit,
        'height_unit': profile.height_unit,
        'calculated_bmr': int(calculated_bmr) if calculated_bmr else None,
        'calculated_calories': int(calculated_calories) if calculated_calories else None,
        'calculated_body_fat': round(calculated_body_fat, 1) if calculated_body_fat else None,
    })
