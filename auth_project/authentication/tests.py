from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from .models import AuthToken

class AuthTokenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_token_creation(self):
        token = AuthToken.create_token(self.user)
        self.assertTrue(token.is_valid)
        self.assertFalse(token.is_expired())
        
        # Token should expire in the future
        self.assertTrue(token.expires_at > timezone.now())
    
    def test_token_validation(self):
        token = AuthToken.create_token(self.user)
        validated_token = AuthToken.validate_token(str(token.token))
        self.assertEqual(validated_token, token)
    
    def test_token_expiration(self):
        token = AuthToken.create_token(self.user)
        
        # Set expiration to the past
        token.expires_at = timezone.now() - datetime.timedelta(hours=1)
        token.save()
        
        # Validation should fail for expired token
        validated_token = AuthToken.validate_token(str(token.token))
        self.assertIsNone(validated_token)
        
        # Token should be marked as invalid after validation attempt
        token.refresh_from_db()
        self.assertFalse(token.is_valid)
    
    def test_token_refresh(self):
        token = AuthToken.create_token(self.user)
        old_expires_at = token.expires_at
        
        # Refresh token with new expiry
        token.refresh(duration_hours=2)
        
        # Expiry should be updated and token should be valid
        self.assertTrue(token.expires_at > old_expires_at)
        self.assertTrue(token.is_valid)