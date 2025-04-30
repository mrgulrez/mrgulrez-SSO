from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import AuthToken

def home(request):
    return render(request, 'authentication/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('validate_auth')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'validate_auth')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'authentication/profile.html')

@login_required
def validate_auth(request):
    # Create an auth token for the logged-in user
    token = AuthToken.create_token(request.user)
    
    # Get the return URL from the query parameters or use a default
    return_url = request.GET.get('next', 'http://localhost:8001/')
    
    # Add the token to the return URL
    if '?' in return_url:
        redirect_url = f"{return_url}&auth_token={token.token}"
    else:
        redirect_url = f"{return_url}?auth_token={token.token}"
    
    return render(request, 'authentication/validate.html', {
        'redirect_url': redirect_url,
        'token': token.token
    })

@csrf_exempt
@require_POST
def validate_token(request):
    try:
        data = json.loads(request.body)
        token_str = data.get('token')
        
        if not token_str:
            return JsonResponse({'valid': False, 'error': 'No token provided'}, status=400)
        
        token = AuthToken.validate_token(token_str)
        
        if token:
            return JsonResponse({
                'valid': True,
                'user_id': token.user.id,
                'username': token.user.username,
                'expires_at': token.expires_at.isoformat()
            })
        else:
            return JsonResponse({'valid': False, 'error': 'Invalid or expired token'}, status=401)
    
    except json.JSONDecodeError:
        return JsonResponse({'valid': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'valid': False, 'error': str(e)}, status=500)

def auth_redirect(request):
    """Handle redirections from the app project with a return URL"""
    return_url = request.GET.get('next', 'http://localhost:8001/')
    login_url = f"/auth/login/?next=/auth/validate/?next={return_url}"
    return redirect(login_url)