from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from .models import Dashboard, Task
from .decorators import login_required

def home(request):
    return render(request, 'main_app/home.html')

@login_required
def dashboard(request):
    # Get or create dashboard for the user
    dashboard, created = Dashboard.objects.get_or_create(
        user_id=request.user.user_id,
        defaults={'username': request.user.username}
    )
    
    # If not created, update the username in case it changed
    if not created:
        dashboard.username = request.user.username
        dashboard.save()
    
    # Get tasks for this dashboard
    tasks = Task.objects.filter(dashboard=dashboard).order_by('-created_at')
    
    return render(request, 'main_app/dashboard.html', {
        'dashboard': dashboard,
        'tasks': tasks
    })

@login_required
def protected_view(request):
    return render(request, 'main_app/protected.html')

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        if title:
            dashboard, _ = Dashboard.objects.get_or_create(
                user_id=request.user.user_id,
                defaults={'username': request.user.username}
            )
            
            Task.objects.create(
                dashboard=dashboard,
                title=title,
                description=description
            )
        
        return redirect('dashboard')
    
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Check if the task belongs to the current user
    if task.dashboard.user_id == request.user.user_id:
        task.delete()
    
    return redirect('dashboard')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Check if the task belongs to the current user
    if task.dashboard.user_id == request.user.user_id:
        task.completed = not task.completed
        task.save()
    
    return redirect('dashboard')

def logout_view(request):
    # Clear the session
    if 'auth_token' in request.session:
        del request.session['auth_token']
    
    if 'user_data' in request.session:
        del request.session['user_data']
    
    # Redirect to the auth service logout page
    return redirect(f"{settings.AUTH_SERVICE_URL}/auth/logout/")