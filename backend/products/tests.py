from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import Product

User = get_user_model()

class BaseClass(TestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(username="testcaseuser", password="test")
        login_url = reverse('login')
        r = self.client.post(login_url, {'username': 'testcaseuser', 'password': 'test'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.token = r.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

class UserTests(BaseClass):
    
    def test_token_retrieval(self):
        """
        Ensure login returns a non-empty token string.
        """
        self.assertIsNotNone(self.token)
        self.assertIsInstance(self.token, str)
        self.assertTrue(len(self.token) > 0)

    def test_protected_endpoint_without_token(self):
        """
        Confirm that accessing a protected endpoint without credentials is unauthorized.
        """
        self.client.credentials()
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_endpoint_with_token(self):
        """
        Confirm that accessing a protected endpoint with a valid token succeeds.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProductViewSetTests(BaseClass):
    """
    This Class is for testing the ProductViewSet found backend.products.views
    """

    def test_retrieve_product_assigned_to_user(self):
        product = Product.objects.create(title="bob", price=10, user=self.user)
        url = reverse("product-detail", args=[product.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product_assigned_to_other_user(self):
        other_user = User.objects.create_user(username="otheruser", password="otherpass")
        product = Product.objects.create(title="bob-other", price=10, user=other_user)
        url = reverse("product-detail", args=[product.id])
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ProductModelTest(BaseClass):
    """
    This Class is for testing the Product Model found backend.products.models
    """

    def test_sale_price_calculations(self):
        product = Product.objects.create(title="Model Test", price=100, user=self.user)
        self.assertEqual(product.sale_price, "80.00")

    def test_get_discount_returns_string(self):
        product = Product.objects.create(title="Model Test", price=100, user=self.user)
        self.assertEqual(product.get_discount(), "122")

    def test_unauthorized_user(self):
        self.client.credentials()
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)