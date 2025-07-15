from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework import status

from products.models import Product


User = get_user_model()
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class BaseClass(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="loginuser", password="pass1234")
        self.client = APIClient()
        self.url = reverse('login')

class LoginTests(BaseClass):
    """
    Tests for the login endpoint at 'login/'.
    """

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

class PermissionsTests(BaseClass):
    """
    Tests for the custom permissions class found in the permissions file
    """ 
    def test_permissions(self):
        user = self.user
        superuser = User.objects.create_superuser(username="suerp", password="superpass")
        
        userProduct = Product.objects.create(
                    title="UserProduct",
                    content="User Content",
                    price=5.0,
                    user=user
                )
        
        superuserProduct = Product.objects.create(
                    title="SuperUserProduct",
                    content="SuperUser content",
                    price=3.0,
                    user=superuser
        )

        # CREATE
        # superuser
        self.client.force_authenticate(user=superuser)
        response = self.client.post("/api/products/", {
                "title": "Test",
                "content": "Test content",
                "price": 10.99
            }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # user
        self.client.force_authenticate(user=user)
        response = self.client.post("/api/products/", {
                "title": "Test",
                "content": "Test content",
                "price": 10.99
            }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # READ
        # superuser
        self.client.force_authenticate(user=superuser)
        response = self.client.get(f"/api/products/{superuserProduct.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user
        self.client.force_authenticate(user=user)
        response = self.client.get(f"/api/products/{userProduct.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # UPDATE
        # superuser
        self.client.force_authenticate(user=superuser)
        response = self.client.put(f"/api/products/{superuserProduct.id}/", {
            "title": "Updated",
            "content": "Updated content",
            "price": 12.99
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # user
        self.client.force_authenticate(user=user)
        response = self.client.put(f"/api/products/{userProduct.id}/", {
            "title": "Updated",
            "content": "Updated content",
            "price": 12.99
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        # superuser
        self.client.force_authenticate(user=superuser)
        response = self.client.delete(f"/api/products/{superuserProduct.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # user
        self.client.force_authenticate(user=user)
        response = self.client.delete(f"/api/products/{userProduct.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)