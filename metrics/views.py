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
    if request.method == 'POST':
        metrics_form = HealthMetricsForm(request.POST, prefix='metrics')
        measurement_form = MeasurementForm(request.POST, prefix='measurement')
        if metrics_form.is_valid():
            m = metrics_form.save(commit=False)
            m.user_profile = profile
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
    })
