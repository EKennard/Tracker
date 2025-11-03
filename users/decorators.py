from functools import wraps
from django.shortcuts import redirect
from users.models import UserProfile

def profile_required(view_func):
    """
    Decorator that checks if the logged-in user has a UserProfile.
    If not, redirects to profile creation page.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            return redirect('create_profile')
        return view_func(request, *args, **kwargs)
    return wrapper
