from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest

from rest_framework.request import Request
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from accounts.permissions import IsSuperUserOrAuthenticatedUser


User = get_user_model()

class LoginTests(APITestCase):
    """
    Tests for the login endpoint at 'login/'.
    """
    def setUp(self):
        # Create a user to authenticate
        self.user = User.objects.create_user(username="loginuser", password="pass1234")
        self.client = APIClient()
        self.url = reverse('login')

    def test_login_success(self):
        """
        A valid username/password pair should return HTTP 200 and a token.
        """
        response = self.client.post(self.url, {
            'username': 'loginuser',
            'password': 'pass1234'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_failure(self):
        """
        An invalid password should return HTTP 400 with an error message.
        """
        response = self.client.post(self.url, {
            'username': 'loginuser',
            'password': 'wrongpass'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class PermissionsTests(APITestCase):
    """
    Tests for the custom permissions class found in the permissions file
    """
    def setUp(self):
        # Create a user to authenticate
        self.user = User.objects.create_user(username="loginuser", password="pass1234")
        self.superuser = User.objects.create_superuser(username="loginsuperuser", password="superpass")
        self.client = APIClient()
        self.url = reverse('login')
    
    def test_authenticated_user_accessing_own_object(self):
        # Simulate user accessing their own object
        class DummyObj:
            owner = self.user

        permission = IsSuperUserOrAuthenticatedUser()

        request = Request(HttpRequest())
        request.user = self.user

        self.client.force_authenticate(user=self.user)
        self.assertTrue(permission.has_object_permission(
            request=request, view=None, obj=DummyObj()))

    def test_authenticated_user_accessing_other_object(self):
        other_user = User.objects.create_user(username="otheruser", password="pass1234")

        class DummyObj:
            owner = other_user

        permission = IsSuperUserOrAuthenticatedUser()

        request = Request(HttpRequest())
        request.user = self.user

        self.assertFalse(permission.has_object_permission(
            request=request, view=None, obj=DummyObj()))

    def test_superuser_accessing_non_superuser_object(self):
        self.client.force_authenticate(user=self.superuser)

        class DummyObj:
            owner = self.user

        permission = IsSuperUserOrAuthenticatedUser()

        request = Request(HttpRequest())
        request.user = self.superuser

        self.assertTrue(permission.has_object_permission(
            request=request, view=None, obj=DummyObj()))

    def test_superuser_accessing_superuser_object(self):
        self.superuser2 = User.objects.create_superuser(username="adminuser2", password="adminpass2")
        self.client.force_authenticate(user=self.superuser)

        class DummyObj:
            owner = self.superuser2

        permission = IsSuperUserOrAuthenticatedUser()

        request = Request(HttpRequest())
        request.user = self.superuser

        self.assertFalse(permission.has_object_permission(
            request=request, view=None, obj=DummyObj()))