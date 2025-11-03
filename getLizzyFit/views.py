from django.shortcuts import render
from datetime import datetime

def home(request):
    return render(request, 'base.html', {'now': datetime.now()})
