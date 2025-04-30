from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='auth_home'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('validate/', views.validate_auth, name='validate_auth'),
    path('api/validate_token/', views.validate_token, name='validate_token'),
    path('redirect/', views.auth_redirect, name='auth_redirect'),
]