from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest

from rest_framework.request import Request
from rest_framework.test import APIClient, APITestCase
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

        crud_accepted_responses = {
                "Create": status.HTTP_201_CREATED, 
                "Read":   status.HTTP_200_OK,
                "Update": status.HTTP_200_OK,
                "Delete": status.HTTP_204_NO_CONTENT,
        }
            
        crud_forbidden_responses = {
                "Create": status.HTTP_403_FORBIDDEN, 
                "Read":   status.HTTP_403_FORBIDDEN,
                "Update": status.HTTP_403_FORBIDDEN,
                "Delete": status.HTTP_403_FORBIDDEN,
        }

        test_cases = [
            {
                "acting_user": user,
                "target_user": user,
                "expected": crud_accepted_responses,
                "desc": "User accessing own object"
            },
            {
                "acting_user": superuser,
                "target_user": user,
                "expected": crud_accepted_responses,
                "desc": "Superuser accessing normal user's object"
            },
            {
                "acting_user": user,
                "target_user": superuser,
                "expected": crud_forbidden_responses,
                "desc": "User accessing superuser's object"
            },
        ]

        for case in test_cases:
            acting_user = case["acting_user"]
            target_user = case["target_user"]
            expected = case["expected"]
            desc = case["desc"]

            self.client.force_authenticate(user=acting_user)

            # Simulate CRUD actions
            print(f"Testing: {desc}")
    
            # Create
            if acting_user==superuser:
                response = self.client.post("/products/", {
                    "title": "Test",
                    "content": "Test content",
                    "price": 10.99
                }, format='json')
                self.assertEqual(response.status_code, expected["Create"])


            # Read
            # Create a product owned by target_user to test Read, Update, Delete
            target_product = userProduct if target_user == user else superuserProduct
            if acting_user == target_user or expected["Read"] not in [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]:
                # Get product
                response = self.client.get(f"/products/{target_product.id}/")
                self.assertEqual(response.status_code, expected["Read"])

                # Update product
                response = self.client.put(f"/products/{target_product.id}/", {
                    "title": "Updated",
                    "content": "Updated content",
                    "price": 12.99
                }, format='json')
                self.assertEqual(response.status_code, expected["Update"])

                # Delete user product
                response = self.client.delete(f"/products/{target_product.id}/")
                self.assertEqual(response.status_code, expected["Delete"])