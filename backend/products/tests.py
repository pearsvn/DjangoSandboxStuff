from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import Product
from .views import ProductViewSet

User = get_user_model()

class UserTests(TestCase):    
    def setUp(self):
        super().setUp()
        user = User.objects.create_user(username="testcaseuser", password="test")
        token = Token.objects.create(user=user)
        self.token_str = str(token)
        self.token_obj = Token.objects.get(key=self.token_str)
        self.token_obj.save()

class ProductViewSetTests(APITestCase):
    """
    This Class is for testing the ProductViewSet found backend.products.views
    """
    def test_retrieve_product_assigned_to_user(self):
        user = User.objects.create_user(username="testcaseuser", password="testpass")
        self.client.force_authenticate(user=user)

        product = Product.objects.create(title="bob", price=10, user=user)
        url = reverse("product-detail", kwargs={"pk": product.pk})
        response = self.client.get(url)
        self.assertEqual(response.data["title"], "bob")
        self.assertEqual(response.data["price"], "10.00")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProductModelTest(APITestCase):
    """
    This Class is for testing the Product Model found backend.products.models
    """
    def setUp(self):
        client = APIClient()
        client.login(username="testcaseuser", password="testpass")
    
    def test_sale_price_calculations(self):
        user = User.objects.create_user(username="modeluser", password="modelpass")
        product = Product.objects.create(title="Model Test", price=100, user=user)
        self.assertEqual(product.sale_price, "80.00")

    def test_get_discount_returns_string(self):
        user = User.objects.create_user(username="modeluser", password="modelpass")
        product = Product.objects.create(title="Model Test", price=100, user=user)
        self.assertEqual(product.get_discount(), "122")

    def test_unauthorized_user(self):
        user = User.objects.create_user(username="modeluser", password="modelpass")
        other_user = User.objects.create_user(username="otheruser", password="otherpass")
        Product.objects.create(title="Mine", price=10, user=user)
        Product.objects.create(title="Not Mine", price=20, user=other_user)
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_accessing_other_user_product(self):
        user = User.objects.create_user(username="modeluser", password="modelpass")
        other_user = User.objects.create_user(username="otheruser", password="otherpass")
        Product.objects.create(title="Mine", price=10, user=user)
        Product.objects.create(title="Not Mine", price=20, user=other_user)
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        