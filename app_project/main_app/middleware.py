from django.conf import settings
from django.shortcuts import redirect
import requests
import json
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

class UserAuthentication:
    def __init__(self, user_id=None, username=None, expires_at=None):
        self.user_id = user_id
        self.username = username
        self.expires_at = expires_at
        self.is_authenticated = user_id is not None and username is not None
    
    def __str__(self):
        if self.is_authenticated:
            return f"User {self.username} (ID: {self.user_id})"
        return "Anonymous User"

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if token is in the URL (redirect from auth service)
        token = request.GET.get('auth_token')
        
        # If token exists in URL, validate and store in session
        if token:
            validated = self.validate_token(token)
            if validated:
                request.session.flush()
                request.session['auth_token'] = token
                request.session['user_data'] = {
                    'user_id': validated['user_id'],
                    'username': validated['username'],
                    'expires_at': validated['expires_at']
                }
        
        # Check if the token is in the session
        if 'auth_token' in request.session and 'user_data' in request.session:
            # Create a user authentication object
            user_data = request.session['user_data']
            request.user = UserAuthentication(
                user_id=user_data['user_id'],
                username=user_data['username'],
                expires_at=user_data['expires_at']
            )
        else:
            # No valid authentication
            request.user = UserAuthentication()
    
    def validate_token(self, token):
        try:
            response = requests.post(
                settings.AUTH_VALIDATE_ENDPOINT,
                json={'token': token},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Token validation error: {e}")
            return None