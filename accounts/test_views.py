from django.test import TestCase
from django.contrib.auth.models import User
from .views import index, login, logout, register
from django.test.client import Client
from django.urls import reverse

class TestViews(TestCase):
    
    # Home Page
    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "index.html")
        
    # Registration Page 
    def test_get_registration_page(self):
        page = self.client.get("/accounts/register/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed("registration.html")
        
    def test_registeration_page_when_logged_in(self):
        user = User.objects.create_user(username='Testing', password='test12345678')
        user.save()
        self.client.login(username='Testing', password='test12345678')
        page = self.client.get("/accounts/register/")
        self.assertEqual(page.status_code, 302)
        
    # Login Page
    def test_login_page_when_logged_in(self):
        user = User.objects.create_user(username='Testing',
        password='test12345678')
        user.save()
        self.client.login(username='Testing', password='test12345678')
        response = self.client.get("/accounts/login/", follow=True)
        self.assertRedirects(response, expected_url=reverse('index'),
        status_code=302, target_status_code=200, fetch_redirect_response=True)
        
    def test_login_page_when_logged_out(self):
        page = self.client.get("/accounts/login/")
        self.assertEqual(page.status_code, 200)
        
    # Logout Page
    def test_logout_page_when_logged_in(self):
        user = User.objects.create_user(username='Testing', password='test12345678')
        user.save()
        self.client.login(username='Testing', password='test12345678')
        response = self.client.get("/accounts/logout/",follow=True)
        for i in response.context['messages']:
            message = str(i)
        
        self.assertEqual(message,'You have successfully been logged out!')
        self.assertRedirects(response, expected_url=reverse('index'),
        status_code=302, target_status_code=200, fetch_redirect_response=True)