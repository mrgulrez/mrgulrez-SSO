from django.conf import settings
from django.shortcuts import redirect
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Get the current path to redirect back after login
            current_path = request.get_full_path()
            
            # Redirect to the auth service
            return redirect(settings.LOGIN_URL)
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view