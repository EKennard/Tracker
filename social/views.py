from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import GroupForm
from users.decorators import profile_required

# Create your views here.

@login_required
@profile_required
def groups(request):
    profile = request.user.userprofile
    groups = profile.groups.all().order_by('name')
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.members.add(profile)
            return redirect('groups')
    else:
        form = GroupForm()
    return render(request, 'social/groups.html', {'form': form, 'groups': groups})
