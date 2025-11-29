from django.shortcuts import render, redirect
from datetime import datetime

def home(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    return render(request, 'base.html', {'now': datetime.now()})
