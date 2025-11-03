from django.shortcuts import render
from django.http import HttpResponse
from .forms import MilestoneForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Milestone
from users.decorators import profile_required

# Create your views here.

@login_required
@profile_required
def milestones_list(request):
    profile = request.user.userprofile
    milestones = Milestone.objects.filter(profile=profile).order_by('-target_date')
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.profile = profile
            milestone.save()
            return redirect('milestones_list')
    else:
        form = MilestoneForm()
    return render(request, 'milestones/milestones_list.html', {'form': form, 'milestones': milestones})
