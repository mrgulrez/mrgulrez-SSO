from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('protected/', views.protected_view, name='protected_view'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('logout/', views.logout_view, name='logout'),
]