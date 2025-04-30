from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import datetime

class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_tokens')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_valid = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Default token expiry time (1 hour)
            self.expires_at = timezone.now() + datetime.timedelta(hours=1)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() >= self.expires_at
    
    def invalidate(self):
        self.is_valid = False
        self.save()
    
    def refresh(self, duration_hours=1):
        self.expires_at = timezone.now() + datetime.timedelta(hours=duration_hours)
        self.is_valid = True
        self.save()
    
    @classmethod
    def create_token(cls, user, duration_hours=1):
        # Invalidate any existing tokens for this user
        user_tokens = cls.objects.filter(user=user, is_valid=True)
        for token in user_tokens:
            token.invalidate()
        
        # Create a new token
        expires_at = timezone.now() + datetime.timedelta(hours=duration_hours)
        return cls.objects.create(user=user, expires_at=expires_at)
    
    @classmethod
    def validate_token(cls, token_str):
        try:
            token_uuid = uuid.UUID(token_str)
            token = cls.objects.get(token=token_uuid, is_valid=True)
            
            if token.is_expired():
                token.invalidate()
                return None
            
            return token
        except (ValueError, cls.DoesNotExist):
            return None
    
    def __str__(self):
        return f"{self.user.username}'s token ({self.token})"