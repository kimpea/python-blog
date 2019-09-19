from django.test import TestCase
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User

# Create your tests here.
class TestForms(TestCase):
    
    # Registration Form Tests
    def test_if_user_can_be_registered(self):
        form = UserRegistrationForm(
            {
                'email': 'test@test.com',
                'username': 'Testing',
                'password1': 'test12345678',
                'password2': 'test12345678',
            }
        )
        self.assertTrue(form.is_valid())
        
    def test_if_user_requires_email(self):
        form = UserRegistrationForm(
            {
                'email': '', 
                'username': 'Testing',
                'password1': 'test123',
                'password2': 'test123',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [u'This field is required.'])
        
    def test_if_user_requires_username(self):
        form = UserRegistrationForm(
            {
                'email': 'test@test.com',
                'username': '',
                'password1': 'test123',
                'password2': 'test123',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])
        
    def test_if_user_requires_password(self):
        form = UserRegistrationForm(
            {
                'email': 'test@test.com', 
                'username': 'Testing',
                'password1': '',
                'password2': '',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password1'], [u'This field is required.'])
        self.assertEqual(form.errors['password2'], [u'This field is required.'])
        
    # Login Form Tests
    def test_if_user_can_be_logged_in(self):
        user = User.objects.create_user(username='Testing', password='test123',
        email='test@test.com')
        user.save()
        form = UserLoginForm({'password': 'test123','username': 'Testing'})
        self.assertTrue(form.is_valid())
        form = UserLoginForm({'password': 'test123','username': 'test@test.com'})
        self.assertTrue(form.is_valid())
        
    def test_if_login_requires_username_and_password(self):
        form = UserLoginForm({'username': 'Testing', 'password': ''})
        self.assertFalse(form.is_valid())
        form = UserLoginForm({'username': '', 'password': 'test123'})
        self.assertFalse(form.is_valid())