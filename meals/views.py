from django.shortcuts import render
from django.http import HttpResponse
from .forms import NutritionLogForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import NutritionLog

# Create your views here.

@login_required
def meal_log(request):
    profile = request.user.userprofile
    logs = NutritionLog.objects.filter(profile=profile).order_by('-date')
    if request.method == 'POST':
        form = NutritionLogForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.profile = profile
            meal.save()
            return redirect('meal_log')
    else:
        form = NutritionLogForm()
    return render(request, 'meals/meal_log.html', {'form': form, 'logs': logs})
