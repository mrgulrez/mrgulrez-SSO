from django.test import TestCase, RequestFactory
from django.conf import settings
from .middleware import AuthenticationMiddleware, UserAuthentication
from .decorators import login_required
from .models import Dashboard, Task
import json
from unittest.mock import patch, MagicMock

class AuthMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = AuthenticationMiddleware(get_response=lambda r: r)
    
    @patch('requests.post')
    def test_middleware_with_token(self, mock_post):
        # Mock the response from the auth service
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'valid': True,
            'user_id': 1,
            'username': 'testuser',
            'expires_at': '2023-01-01T00:00:00Z'
        }
        mock_post.return_value = mock_response
        
        # Create a request with a token
        request = self.factory.get('/?auth_token=valid_token')
        request.session = {}
        
        # Process the request with middleware
        self.middleware.process_request(request)
        
        # Check that the session was updated
        self.assertEqual(request.session['auth_token'], 'valid_token')
        self.assertEqual(request.session['user_data']['user_id'], 1)
        self.assertEqual(request.session['user_data']['username'], 'testuser')
        
        # Check that the user attribute was set
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(request.user.username, 'testuser')

class LoginRequiredDecoratorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_redirect_anonymous_user(self):
        @login_required
        def test_view(request):
            return "View accessed"
        
        request = self.factory.get('/protected/')
        request.user = UserAuthentication()  # Anonymous user
        
        response = test_view(request)
        
        # Check that we got redirected to the login URL
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.LOGIN_URL in response.url)
    
    def test_allow_authenticated_user(self):
        @login_required
        def test_view(request):
            return "View accessed"
        
        request = self.factory.get('/protected/')
        request.user = UserAuthentication(user_id=1, username='testuser', expires_at='2023-01-01T00:00:00Z')
        
        response = test_view(request)
        
        # Check that the view was accessed
        self.assertEqual(response, "View accessed")

class DashboardModelTest(TestCase):
    def test_dashboard_creation(self):
        dashboard = Dashboard.objects.create(
            user_id=1,
            username='testuser'
        )
        
        self.assertEqual(dashboard.user_id, 1)
        self.assertEqual(dashboard.username, 'testuser')
        self.assertEqual(str(dashboard), "testuser's Dashboard")
    
    def test_task_creation(self):
        dashboard = Dashboard.objects.create(
            user_id=1,
            username='testuser'
        )
        
        task = Task.objects.create(
            dashboard=dashboard,
            title='Test Task',
            description='Task description'
        )
        
        self.assertEqual(task.dashboard, dashboard)
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Task description')
        self.assertFalse(task.completed)
        self.assertEqual(str(task), 'Test Task')