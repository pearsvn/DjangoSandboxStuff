from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest

from rest_framework.request import Request
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from accounts.permissions import IsSuperUserOrAuthenticatedUser

from products.models import Product


User = get_user_model()

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
    # def test_authenticated_user_accessing_own_object(self):
    #     # Simulate user accessing their own object
    #     class DummyObj:
    #         owner = self.user

    #     permission = IsSuperUserOrAuthenticatedUser()

    #     request = Request(HttpRequest())
    #     request.user = self.user

    #     self.client.force_authenticate(user=self.user)
    #     self.assertTrue(permission.has_object_permission(
    #         request=request, view=None, obj=DummyObj()))

    # def test_authenticated_user_accessing_other_object(self):
    #     other_user = User.objects.create_user(username="otheruser", password="pass1234")

    #     class DummyObj:
    #         owner = other_user

    #     permission = IsSuperUserOrAuthenticatedUser()

    #     request = Request(HttpRequest())
    #     request.user = self.user

    #     self.assertFalse(permission.has_object_permission(
    #         request=request, view=None, obj=DummyObj()))

    # def test_superuser_accessing_non_superuser_object(self):
    #     self.client.force_authenticate(user=self.superuser)

    #     class DummyObj:
    #         owner = self.user

    #     permission = IsSuperUserOrAuthenticatedUser()

    #     request = Request(HttpRequest())
    #     request.user = self.superuser

    #     self.assertTrue(permission.has_object_permission(
    #         request=request, view=None, obj=DummyObj()))

    # def test_superuser_accessing_superuser_object(self):
    #     self.superuser2 = User.objects.create_superuser(username="adminuser2", password="adminpass2")
    #     self.client.force_authenticate(user=self.superuser)

    #     class DummyObj:
    #         owner = self.superuser2

    #     permission = IsSuperUserOrAuthenticatedUser()

    #     request = Request(HttpRequest())
    #     request.user = self.superuser

    #     self.assertFalse(permission.has_object_permission(
    #         request=request, view=None, obj=DummyObj()))
        
    def test_permissions(self):
        user = self.user
        superuser = self.user
        another_user = User.objects.create_user(username="anotherUser", password="anotherUserPass")
        another_superuser = User.objects.create_superuser(username="anotherSuperuser", password="anotherSuperpass")

        # povs = [user, superuser, another_user, another_superuser ]
        crud_accepted_responses = {
                "Create": status.HTTP_201_CREATED, 
                "Read":   status.HTTP_200_OK,
                "Update": status.HTTP_200_OK,
                "Delete": status.HTTP_204_NO_CONTENT,
        }
            
        crud_not_found_responses = {
                "Create": status.HTTP_404_NOT_FOUND, 
                "Read":   status.HTTP_404_NOT_FOUND,
                "Update": status.HTTP_404_NOT_FOUND,
                "Delete": status.HTTP_404_NOT_FOUND,
        }

        test_cases = [
            {
                "acting_user": user,
                "target_user": another_user,
                "expected": crud_not_found_responses,
                "desc": "User accessing another user's object"
            },
            {
                "acting_user": user,
                "target_user": user,
                "expected": crud_accepted_responses,
                "desc": "User accessing own object"
            },
            {
                "acting_user": another_user,
                "target_user": user,
                "expected": crud_not_found_responses,
                "desc": "Another user accessing user's object"
            },
            {
                "acting_user": another_superuser,
                "target_user": user,
                "expected": crud_accepted_responses,
                "desc": "Superuser accessing normal user's object"
            },
            {
                "acting_user": another_superuser,
                "target_user": another_superuser,
                "expected": crud_accepted_responses,
                "desc": "Superuser accessing own object"
            },
            {
                "acting_user": another_superuser,
                "target_user": superuser,
                "expected": crud_not_found_responses,
                "desc": "Superuser accessing another superuser's object"
            }
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
            if acting_user == target_user or acting_user==IsSuperUserOrAuthenticatedUser:
                response = self.client.post("/products/", {
                    "title": "Test",
                    "content": "Test content",
                    "price": 10.99
                }, format='json')
                self.assertEqual(response.status_code, expected["Create"])
            else:
                return status.HTTP_404_NOT_FOUND

            # Read
            # Create a product owned by target_user to test Read, Update, Delete
            if acting_user == target_user or expected["Read"] != status.HTTP_404_NOT_FOUND:
                product = Product.objects.create(
                    title="ReadTest",
                    content="Read Content",
                    price=5.0,
                    user=target_user
                )
                response = self.client.get(f"/products/{product.id}/")
                self.assertEqual(response.status_code, expected["Read"])

                # Update
                response = self.client.put(f"/products/{product.id}/", {
                    "title": "Updated",
                    "content": "Updated content",
                    "price": 12.99
                }, format='json')
                self.assertEqual(response.status_code, expected["Update"])

                # Delete
                response = self.client.delete(f"/products/{product.id}/")
                self.assertEqual(response.status_code, expected["Delete"])