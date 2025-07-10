from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

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
